import pygame

from rtsgame.src.Client.UI.Widget import Widget
from rtsgame.src.utility.utilities import Vector


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.sio = None

    def draw(self, surface: pygame.Surface, abs_position: Vector = Vector(0, 0)):
        super().draw(surface, abs_position)

    def accept_events(self, events):
        for event in events:
            self.accept_event(event)

    def accept_event(self, event):
        pass

    def accept_action(self, action):
        pass

    def set_sio(self, sio):
        self.sio = sio
