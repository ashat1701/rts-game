import pygame
from src.utility.utilities import Vector
from src.Client.UI.Widget import Widget


class Window(Widget):
    def __init__(self):
        super().__init__()

    def draw(self, surface: pygame.Surface, abs_position: Vector=Vector(0,0)):
        super().draw(surface, abs_position)

    def accept_events(self, events):
        for event in events:
            self.accept_event(event)

    def accept_event(self, event):
        pass