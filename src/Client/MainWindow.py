import pygame
import logging

from src.Client.Camera import Camera
from src.Client.EntitySprite import EntitySprite
from src.Client.UI.Window import Window
from src.utility.utilities import Vector
from src.utility.utilities import level_to_tile


class MainWindow(Window):
    def __init__(self, size, client=None):
        super().__init__()
        self.client = client
        self.entities = []

        self.main_camera = Camera(Vector(0, 0), size)
        self.add_child(self.main_camera, Vector(0, 0))

    def set_client(self, client):
        self.client = client

    def accept_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.client.send_object("MOVE_RIGHT")
            elif event.key == pygame.K_LEFT:
                self.client.send_object("MOVE_LEFT")
            elif event.key == pygame.K_DOWN:
                self.client.send_object("MOVE_DOWN")
            elif event.key == pygame.K_UP:
                self.client.send_object("MOVE_UP")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.client.send_object("STOP_MOVE_RIGHT")
            elif event.key == pygame.K_LEFT:
                self.client.send_object("STOP_MOVE_LEFT")
            elif event.key == pygame.K_DOWN:
                self.client.send_object("STOP_MOVE_DOWN")
            elif event.key == pygame.K_UP:
                self.client.send_object("STOP_MOVE_UP")

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
            for entity in self.entities:
                if entity.type == 'player':
                    self.main_camera.set_center(entity.position)
            self.main_camera.set_sprites(self.entities)
