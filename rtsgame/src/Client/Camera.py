from itertools import chain
from typing import Union

import pygame

from rtsgame.src.Client.HPBar import HPBar
from rtsgame.src.Client.TileSprite import TileSprite
from rtsgame.src.Client.UI.Widget import Widget
from rtsgame.src.utility.constants import PLAYER_HEALTH
from rtsgame.src.utility.utilities import Vector


class Camera(Widget):
    def __init__(self, world_camera_position: Vector, size):
        super().__init__()
        self._box = pygame.Rect(world_camera_position, size)
        self._sprites = []
        self._tiles = []
        self.hpbar = HPBar(PLAYER_HEALTH, PLAYER_HEALTH)
        self.add_child(self.hpbar, Vector(0, -100))

    @property
    def size(self):
        return Vector(*self._box.size)

    def draw(self, surface: pygame.Surface,
             abs_position: Union[Vector, tuple]):
        world_pos = Vector(*self._box.topleft)

        for sprite in chain(self._tiles, self._sprites):
            if not self.is_visible(sprite):
                continue

            rel_pos = sprite.position - world_pos
            abs_child_pos = abs_position + rel_pos
            sprite.draw(surface, abs_child_pos)

        super().draw(surface, abs_position)

    def set_sprites(self, sprites):
        self._sprites = sprites

    def set_center(self, world_position: Vector):
        self._box.center = world_position

    def set_map(self, tile_map):
        self._tiles = []
        for i, row in enumerate(tile_map):
            for j, tile_type in enumerate(row):
                self._tiles.append(TileSprite(tile_type, j, i))

    def set_hp(self, cur_hp):
        self.hpbar.hp = cur_hp

    def is_visible(self, sprite):
        if sprite.box is None:
            return True

        return self._box.colliderect(sprite.box)
