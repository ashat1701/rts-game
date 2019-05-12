from threading import Thread

import socketio

from rtsgame.src.Client.Game import game
from rtsgame.src.utility.constants import PORT

sio = socketio.Client()
sio_thread = None

@sio.on('message')
def accept_action(data):
    game.accept_action(data)


@sio.on('connect')
def on_connect():
    sio.emit('message', 'PLAYER_CONNECTED')


@sio.on('disconnect')
def on_disconnect():
    game.running = False
    exit(0)


def run(ip):
    global sio_thread
    sio.connect(f"http://{ip}:{PORT}")

    sio_thread = Thread(target=sio.wait)
    sio_thread.setDaemon(True)
    sio_thread.start()
