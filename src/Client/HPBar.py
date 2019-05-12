import pygame

from src.Client.UI.Widget import Container
from src.utility.utilities import Vector, load_sprites, join_paths


class HPBar(Container):
    sprites = load_sprites(
        join_paths('src/Client/HUD/HP/Value', ['HP_Value_0.png',
                                               'HP_Value_1.png',
                                               'HP_Value_2.png',
                                               'HP_Value_3.png',
                                               'HP_Value_4.png',
                                               'HP_Value_5.png', ]))

    def __init__(self, cur_hp, max_hp):
        super().__init__()
        self.hp = cur_hp
        self.max_hp = max_hp

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        sprite_num = self.get_sprite_num()
        surface.blit(self.sprites[sprite_num], abs_position)

    def get_sprite_num(self):
        return int(self.hp / self.max_hp * (len(self.sprites) - 1))
