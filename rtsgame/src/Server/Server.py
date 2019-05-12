import logging
import queue
from threading import Thread

import eventlet
import socketio

from rtsgame.src.utility.constants import PORT

player_disconnected = False


class Server:
    def __init__(self, port=PORT):
        super().__init__()
        self.action_queue = queue.Queue()
        self.connections = {}
        self.rconnections = {}
        self.activeConnections = 0
        self.sio = socketio.Server(async_mode='eventlet')
        self.app = socketio.WSGIApp(self.sio)
        self.port = port

        self.sio.on('message')(self.on_message)
        self.sio.on('connect')(self.on_connect)
        self.sio.on('disconnect')(self.on_disconnect)

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

    def on_disconnect(self, sid):
        global player_disconnected
        player_disconnected = True

    def send_obj_all_players(self, obj):
        for player_id in range(len(self.connections)):
            self.send_obj_to_player(obj, player_id)

    def start(self):
        thread = Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()

    def run(self):
        try:
            eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)
        except Exception as e:
            logging.error("Error in server {}".format(e))
            raise e

    def send_obj_to_player(self, obj, player_id):
        self.sio.emit("message", obj, self.connections[player_id])
