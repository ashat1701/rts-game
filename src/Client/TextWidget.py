from src.Client.UI.Window import Window
from src.Client.UI.Widget import Widget
import pygame
from src.utility.utilities import Vector
import logging


class TextWidget(Widget):
    def __init__(self, text):
        super().__init__()
        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = text
        self.text_surface = font.render(text, False, (255, 255, 255))
        self.text_surface = self.text_surface.convert_alpha()

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        print(self.text, abs_position)
        surface.blit(self.text_surface, abs_position)
