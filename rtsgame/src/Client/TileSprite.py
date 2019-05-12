import pygame

from rtsgame.src.Client.Sprite import Sprite
from rtsgame.src.utility.constants import WALL, STONE, FLOOR, PIXEL_SCALE
from rtsgame.src.utility.utilities import Vector

_surfaces = {
    WALL: {
        0: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE)),
        1: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
    },
    FLOOR: {
        0: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE)),
        1: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
    },
    STONE: {
        0: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE)),
        1: pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
    }
}

_surfaces[WALL][0].fill((100, 100, 100))
_surfaces[WALL][1].fill((100, 100, 100))
_surfaces[FLOOR][0].fill((100, 0, 0))
_surfaces[FLOOR][1].fill((100, 0, 0))
_surfaces[STONE][0].fill((100, 100, 0))
_surfaces[STONE][1].fill((100, 100, 0))

pygame.draw.rect(_surfaces[WALL][1], (255, 0, 0),
                 (0, 0, PIXEL_SCALE, PIXEL_SCALE))
pygame.draw.rect(_surfaces[FLOOR][1], (255, 0, 0),
                 (0, 0, PIXEL_SCALE, PIXEL_SCALE))
pygame.draw.rect(_surfaces[STONE][1], (255, 0, 0),
                 (0, 0, PIXEL_SCALE, PIXEL_SCALE))

_surfaces[WALL][0] = _surfaces[WALL][0].convert_alpha()
_surfaces[WALL][1] = _surfaces[WALL][1].convert_alpha()
_surfaces[FLOOR][0] = _surfaces[FLOOR][0].convert_alpha()
_surfaces[FLOOR][1] = _surfaces[FLOOR][1].convert_alpha()
_surfaces[STONE][0] = _surfaces[STONE][0].convert_alpha()
_surfaces[STONE][1] = _surfaces[STONE][1].convert_alpha()


class TileSprite(Sprite):
    def __init__(self, tile_type, col, row, tile_state=0):
        super().__init__()
        self.tile_type = tile_type
        self.tile_state = tile_state
        self.col = col
        self.row = row
        self.box = pygame.Rect(self.row * PIXEL_SCALE, self.col * PIXEL_SCALE,
                               PIXEL_SCALE, PIXEL_SCALE)

    def set_visible(self):
        self.tile_state = 1

    @property
    def x(self):
        return self.box.left

    @property
    def y(self):
        return self.box.top

    @property
    def position(self):
        return Vector(*self.box.topleft)

    @property
    def sprite(self):
        return _surfaces[self.tile_type][self.tile_state]

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        surface.blit(self.sprite, abs_position)

        super().draw(surface, abs_position)
