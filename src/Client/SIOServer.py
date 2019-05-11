from threading import Thread

import socketio

from src.Client.Game import game

sio = socketio.Client()


@sio.on('message')
def accept_action(data):
    game.accept_action(data)


@sio.on('connect')
def on_connect():
    sio.emit('message', 'PLAYER_CONNECTED')


def run():
    sio.connect('http://localhost:8080')

    sio_thread = Thread(target=sio.wait)
    sio_thread.start()
