from threading import Thread

import socketio

from src.Client.Game import game
from src.utility.constants import PORT

sio = socketio.Client()


@sio.on('message')
def accept_action(data):
    game.accept_action(data)

@sio.on('connect')
def on_connect():
    sio.emit('message', 'PLAYER_CONNECTED')

@sio.on('disconnect')
def on_disconnect():
    game.running = False


def run(ip):
    sio.connect(f"http://{ip}:{PORT}")

    sio_thread = Thread(target=sio.wait)
    sio_thread.setDaemon(True)
    sio_thread.start()
