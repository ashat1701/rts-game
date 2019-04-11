import socket
import threading
import sys
import pickle
import logging
import queue

class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    players = {}
    threads = []
    action_queue = queue.Queue()
    activeConnections = 0

    def __init__(self, port=8080):
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)

    def handler(self, connection, addr):
        while True:
            try:
                data = connection.recv(4096)
            except ConnectionError as exc:
                player_id = self.players[addr[0]]
                self.activeConnections -= 1
                logging.debug("player # {} - disconnected".format(player_id))
                self.connections[player_id] = None
                break
            host = addr[0]
            if not data:
                player_id = self.players[host]
                self.activeConnections -= 1
                logging.debug("player # {} - disconnected".format(player_id))
                self.connections[player_id] = None
                break
            obj = pickle.loads(data)
            self.action_queue.put((self.players[host], obj))
            logging.debug("object receive from {}, addr {}, obj {}".format(str(self.players[host]), str(host), str(obj)))

    def send_obj_all_players(self, obj):
        for player_id in range(len(self.connections)):
            self.send_obj_to_player(obj, player_id)

    def run(self):
        while True:
            connection, addr = self.server_socket.accept()
            new_thread = threading.Thread(target=self.handler, args=(connection, addr))
            new_thread.daemon = True
            self.activeConnections += 1
            if addr[0] in self.players:
                self.connections[self.players[addr[0]]] = connection
                self.threads[self.players[addr[0]]] = new_thread
            else:
                self.connections.append(connection)
                self.threads.append(new_thread)
                self.players[addr[0]] = len(self.players)
            logging.debug("player # {} connected".format(str(self.players[addr[0]])))
            new_thread.start()  

    def send_obj_to_player(self, obj, player_id):
        if player_id < len(self.connections) and self.connections[player_id] is not None:
            self.connections[player_id].send(pickle.dumps(obj))
            return True
        return False


class SafeServer(Server):
    def __init__(self, port=8080):
        super().__init__(port)

    def __enter__(self):
        return self

    def start_as_daemon(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def __exit__(self, exc_type, exc_tb):
        for conn in self.connections:
            if conn is not None:
                conn.close()
        self.server_socket.close()


def run():
    with SafeServer() as server:
        server.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()