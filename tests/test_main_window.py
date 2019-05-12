import pygame
import sys

import os
os.chdir("..")


class FakeDummy:
    def __init__(self, *args):
        pass


fake_game_module = FakeDummy()
fake_game_module.game = FakeDummy
sys.modules['src.Client.Game'] = fake_game_module
fake_camera_module = FakeDummy()
fake_camera_module.Camera = FakeDummy
sys.modules['src.Client.Camera'] = fake_camera_module

from src.Client.MainWindow import MainWindow


def test_attack():
    fake_sio = FakeDummy()

    def fake_emit(name, data):
        assert name == 'message'
        assert data == 'ATTACK'

    fake_sio.emit = fake_emit

    main_window = MainWindow((100, 100), fake_sio)

    event = FakeDummy()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_f
    main_window.accept_event(event)


del sys.modules['src.Client.Game']
del sys.modules['src.Client.Camera']
