import logging
import pickle
import queue
import socket
import time
import threading
import socketio
import eventlet
from src.utility.constants import PORT


class Server:
    action_queue = queue.Queue()
    connections = {} # map player_id to cid
    rconnections = {} #map cid to player_id
    activeConnections = 0
    sio = socketio.Server(async_mode='eventlet')
    app = socketio.Middleware(sio)



    def __init__(self, port=PORT):
        self.port = port

    @staticmethod
    @sio.on("message")
    def on_message(sid, *data):
        #todo : ПОДУМАТЬ
        if len(data) == 1:
            server.action_queue.put((server.rconnections[sid], data[0]))
        else:
            server.action_queue.put((server.rconnections[sid], data))

    @staticmethod
    @sio.on("connect")
    def on_connect(sid, environ):
        server.connections[server.activeConnections] = sid
        server.rconnections[sid] = server.activeConnections
        server.activeConnections += 1

    def send_obj_all_players(self, obj):
        for player_id in range(len(self.connections)):
            self.send_obj_to_player(obj, player_id)

    def run(self):
        try:
            eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)
        except Exception as e:
            logging.error("Error in server {}".format(e))
            raise e


    def send_obj_to_player(self, obj, player_id):
        if player_id < len(self.connections) and self.connections[
            player_id] is not None:
            self.sio.emit("message", obj, room=self.connections[player_id])
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
        if exc_val:
            raise ChildProcessError("Safe sere")

def run():
    with SafeServer() as server:
        server.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()

server = SafeServer()