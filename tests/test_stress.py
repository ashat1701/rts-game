import os
import time
from queue import Queue
import pygame
os.chdir("..")


import src.utility.constants
from src.Client.Camera import Camera
from src.Client.EntitySprite import EntitySprite
from src.utility.utilities import Vector

from App import App


class FakeDummy:
    def __init__(self, *args):
        pass


def pass_func(*args, **kwargs):
    pass


fake_server = FakeDummy()
fake_server.action_queue = Queue()
fake_server.send_obj_to_player = pass_func


def test_update_time():
    src.utility.constants.ROOMS = 10
    app = App(fake_server)
    app.logic.spawn_system.create_player(0)
    for i in range(400):
        app.logic.spawn_system.create_enemy()

    start = time.time()
    for i in range(100):
        try:
            app.update()
        except SystemExit:
            pass
    delta = time.time() - start
    assert delta / 100 < 0.1


def test_animation_system():
    app = App(fake_server)
    app.logic.spawn_system.create_player(0)
    anim_system = app.logic.animation_system

    anim_system.add_entity(0)

    start = time.time()
    for i in range(int(1000)):
        anim_system.get_animation_state(0)
    delta = time.time() - start
    assert delta < 0.005


def get_sprites(num):
    info = ((100, 200),
            'player1',
            'idle',
            0,
            (10, 100))
    return [EntitySprite(info) for _ in range(num)]


def test_drawing_entities():
    from src.Client.EntitySprite import EntitySpriteManager
    EntitySpriteManager.load_entity_config(
        'src/utility/animations/player1_animations.json')
    camera = Camera(Vector(0, 0), Vector(1000, 1000))
    surface = pygame.Surface((1000, 1000))

    camera.set_sprites(get_sprites(500))

    start = time.time()
    for i in range(int(100)):
        camera.draw(surface, Vector(0, 0))
    delta = time.time() - start

    assert delta / 100 < 0.05
