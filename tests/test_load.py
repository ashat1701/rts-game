import os
import time
from queue import Queue

from App import App

os.chdir("..")


class FakeDummy:
    def __init__(self, *args):
        pass


def pass_func(*args, **kwargs):
    pass


fake_server = FakeDummy()
fake_server.action_queue = Queue()
fake_server.send_obj_to_player = pass_func


def test_update_time():
    app = App(fake_server)
    app.logic.spawn_system.create_player(0)
    for i in range(15):
        app.logic.spawn_system.create_enemy()

    start = time.time()
    for i in range(100):
        app.update()
    delta = time.time() - start
    assert delta / 100 < 0.005
