import logging
from typing import Union

import pygame

from src.Client.UI.EntitySprite import EntitySprite
from src.Client.UI.Widget import Widget
from src.utility.utilities import Vector


class Camera(Widget):
    def __init__(self, world_camera_position: Vector, size: Vector):
        super().__init__()
        self.world_position = world_camera_position
        self.size = size
        self.sprites = []

    def draw(self, surface: pygame.Surface,
             abs_position: Union[Vector, tuple]):
        for sprite in self.sprites:
            rel_pos = sprite.position - self.world_position
            abs_child_pos = abs_position + rel_pos

            sprite.draw(surface, abs_child_pos)
        # TODO Draw terrain
        super().draw(surface, abs_position)

    def set_sprites(self, sprites):
        self.sprites = sprites

    def add_sprite(self, sprite):
        if not isinstance(sprite, EntitySprite):
            raise RuntimeError("Camera can only accept sprites")
        id_ = id(sprite)

        if id_ in self.sprites:
            raise RuntimeError("Sprite {} is already connected as child"
                               .format(id_))
        self.sprites[id_] = sprite
        logging.info("Added sprite to a camera")

    def remove_sprite(self, sprite):
        id_ = id(sprite)
        del self.sprites[id_]

    def update_watch_point(self, world_position: Vector):
        new_position = world_position - self.size / 2

    def move_to(self, new_position: Vector):
        self.world_position = new_position
