import socketio
from threading import Thread
from src.Client.Game import game

sio = socketio.Client()


@sio.on('message')
def accept_action(data):
    game.accept_action(data)


def run():
    sio.connect('http://localhost:5000')

    sio_thread = Thread(target=sio.wait)
    sio_thread.start()



