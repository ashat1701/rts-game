import socket
import threading
import sys
import pickle
import logging
import queue
from src.utility.constants import PORT


class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    threads = []
    action_queue = queue.Queue()
    activeConnections = 0

    def __init__(self, port=PORT):
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)

    def handler(self, connection, player_id):
        while True:
            try:
                data = connection.recv(4096)
            except ConnectionError as exc:
                self.activeConnections -= 1
                logging.info("player # {} - disconnected".format(player_id))
                self.connections[player_id].close()
                self.connections[player_id] = None
                break
            if not data:
                self.activeConnections -= 1
                logging.info("player # {} - disconnected".format(player_id))
                self.connections[player_id].close()
                self.connections[player_id] = None
                break
            obj = pickle.loads(data)
            logging.debug("received1 - {}".format(obj))
            self.action_queue.put((player_id, obj[1]))

    def send_obj_all_players(self, obj):
        for player_id in range(len(self.connections)):
            self.send_obj_to_player(obj, player_id)

    def run(self):
        try:
            while True:
                connection, addr = self.server_socket.accept()
                data = connection.recv(4096)
                query = pickle.loads(data)[1]
                logging.debug("received - {}".format(query))
                self.activeConnections += 1
                if query == "ACTION_GET_ID":
                    new_thread = threading.Thread(target=self.handler, args=(connection, len(self.connections)))
                    self.connections.append(connection)
                    new_thread.daemon = True
                    self.threads.append(new_thread)
                    self.send_obj_to_player(len(self.connections) - 1, len(self.connections) - 1)
                    logging.info("player # {} connected".format(len(self.connections) - 1))
                    self.action_queue.put((len(self.connections) - 1, "PLAYER_CONNECTED"))
                    new_thread.start()
                else:
                    str, client_id = query.split(':')
                    client_id = int(client_id)
                    self.connections[client_id] = connection
                    new_thread = threading.Thread(target=self.handler, args=(connection, client_id))
                    new_thread.daemon = True
                    self.threads[client_id] = new_thread
                    logging.info("player # {} reconnected".format(client_id))
                    new_thread.start()
        finally:
            for i in self.connections:
                if i is not None:
                    i.close()
            self.server_socket.close()

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        for conn in self.connections:
            if conn is not None:
                conn.close()
        self.server_socket.close()
        if exc_val:
            raise


def run():
    with SafeServer() as server:
        server.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()