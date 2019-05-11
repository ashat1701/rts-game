import logging
import pickle
import queue
import socket
import time
import threading
import socketio
import eventlet
from src.utility.constants import PORT
from threading import Thread


class Server:
    def __init__(self, port=PORT):
        super().__init__()
        self.action_queue = queue.Queue()
        self.connections = {}  # map player_id to cid
        self.rconnections = {}  # map cid to player_id
        self.activeConnections = 0
        self.sio = socketio.Server(async_mode='eventlet')
        self.app = socketio.WSGIApp(self.sio)
        self.port = port

        self.sio.on('message')(self.on_message)
        self.sio.on('connect')(self.on_connect)

    def on_message(self, sid, *data):
        # todo : ПОДУМАТЬ
        if len(data) == 1:
            self.action_queue.put((self.rconnections[sid], data[0]))
        else:
            self.action_queue.put((self.rconnections[sid], data))

    def on_connect(self, sid, environ):
        self.connections[self.activeConnections] = sid
        self.rconnections[sid] = self.activeConnections
        self.activeConnections += 1

    def send_obj_all_players(self, obj):
        for player_id in range(len(self.connections)):
            self.send_obj_to_player(obj, player_id)

    def start(self):
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        try:
            eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)
        except Exception as e:
            logging.error("Error in server {}".format(e))
            raise e

    def send_obj_to_player(self, obj, player_id):
        self.sio.emit("message", obj, self.connections[player_id])
