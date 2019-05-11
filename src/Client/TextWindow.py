from src.Client.UI.Window import Window
import pygame
from src.utility.utilities import Vector
import logging


class TextWindow(Window):
    def __init__(self, text, position):
        super().__init__()
        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = font.render(text, False, (255, 255, 255))
        self.text_surface = self.text_surface.convert_alpha()
        self.position = position

    def draw(self, surface: pygame.Surface,
             abs_position: Vector = Vector(0, 0)):
        surface.blit(self.text_surface, abs_position + self.position)


class WaitWindow(TextWindow):
    def __init__(self):
        super().__init__('Waiting for other players.', Vector(1000, 1000) / 2)
        self.map = None

    def accept_action(self, action):
        if not isinstance(action, list):
            raise RuntimeError(
                "Action is not of type list. Don't know what to do with it")

        if action[0] == "MAP":
            self.map = action[1]
            logging.info("Acquired map")
            self.sio.emit("message", "MAP_RECEIVED")

        if action[0] == "START_GAME":
            from src.Client.Game import game
            game.start_main_window(self.map)
