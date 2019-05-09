import pygame
from src.utility.utilities import Vector
from abc import ABCMeta, abstractmethod
from src.Client.UI.Widget import Widget


class Sprite(Widget, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.box = None

    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def sprite(self):
        pass

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        surface.blit(self.sprite, abs_position)

        super().draw(surface, abs_position)
