import pygame

from src.Client.Camera import Camera
from src.Client.EntitySprite import EntitySprite
from src.Client.UI.Window import Window
from src.utility.utilities import Vector


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

        self.entities = [EntitySprite(info) for info in action]
        self.main_camera.set_sprites(self.entities)
