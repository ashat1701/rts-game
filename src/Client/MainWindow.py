import pygame
import logging

from src.Client.Camera import Camera
from src.Client.EntitySprite import EntitySprite
from src.Client.UI.Window import Window
from src.utility.utilities import Vector
from src.utility.constants import MOVE_UPDATE


class MainWindow(Window):
    def __init__(self, size, client=None):
        super().__init__()
        self.client = client
        self.entities = []

        self.main_camera = Camera(Vector(0, 0), size)
        self.add_child(self.main_camera, Vector(0, 0))
        pygame.time.set_timer(pygame.USEREVENT, MOVE_UPDATE)

    def set_client(self, client):
        self.client = client

    def accept_event(self, event):
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

            self.client.send_object(("MOVE", tuple(direction)))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.client.send_object("ATTACK")

    def accept_action(self, action):
        if not isinstance(action, list):
            raise RuntimeError(
                "Action is not of type list. Don't know what to do with it")
        if action[0] == "MAP":
            # self.main_camera.level = action[1]
            # self.main_camera.map_tile = level_to_tile(action[1])
            self.main_camera.set_map(action[1])
            logging.info("Initialized map")
        else:
            self.entities = [EntitySprite(info) for info in action]
            self.main_camera.set_center(self.entities[0].position)
            self.main_camera.set_sprites(self.entities)
