import logging

import pygame

from rtsgame.src.utility.utilities import Vector


class Widget:
    def __init__(self):
        self.children = {}

    def add_child(self, child, position: Vector):
        id_ = id(child)

        if id_ in self.children:
            raise RuntimeError("Child {} is already connected as child"
                               .format(id_))
        self.children[id_] = (child, position)
        logging.info("Added child")

    def remove_child(self, child):
        id_ = id(child)
        del self.children[id_]

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        # TODO blit background
        for child, rel_pos in self.children.values():
            child.draw(surface, abs_position + rel_pos)
