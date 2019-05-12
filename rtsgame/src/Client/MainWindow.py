from threading import Lock

import pygame

from rtsgame.src.Client.Camera import Camera
from rtsgame.src.Client.EntitySprite import EntitySprite
from rtsgame.src.Client.TextWidget import TextWidget
from rtsgame.src.Client.UI.Window import Window
from rtsgame.src.utility.constants import MOVE_UPDATE
from rtsgame.src.utility.utilities import Vector


class MainWindow(Window):
    def __init__(self, size, sio=None):
        super().__init__()
        self.sio = sio
        self.entities = []
        self.lock = Lock()
        self.main_camera = Camera(Vector(0, 0), size)
        self.add_child(self.main_camera, Vector(0, 0))
        self.spectate = False
        pygame.time.set_timer(pygame.USEREVENT, MOVE_UPDATE)

    def accept_event(self, event):
        if self.spectate:
            return

        if event.type == pygame.USEREVENT:
            state = pygame.key.get_pressed()
            direction = Vector(0, 0)

            if state[pygame.K_w]:
                direction += Vector(0, -1)
            if state[pygame.K_s]:
                direction += Vector(0, 1)
            if state[pygame.K_d]:
                direction += Vector(1, 0)
            if state[pygame.K_a]:
                direction += Vector(-1, 0)

            self.sio.emit('message', ("MOVE", tuple(direction)))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.sio.emit('message', "ATTACK")

    def enable_spectate(self):
        spectate_text = TextWidget('Spectating')
        self.main_camera.add_child(spectate_text, Vector(0, 900))

        self.spectate = True

    def accept_action(self, action):
        if not isinstance(action, list):
            raise RuntimeError(
                "Action is not of type list. Don't know what to do with it")

        if action[0] == 'SPECTATE':
            self.enable_spectate()
        else:
            self.entities = [EntitySprite(info) for info in action]
            with self.lock:
                self.main_camera.set_hp(self.entities[0].health)
                self.main_camera.set_center(self.entities[0].position)
                self.main_camera.set_sprites(self.entities)
