import pygame
from src.Client.Animation import Animation, parse_config
from src.utility.utilities import cls_init
from typing import Tuple


class EntitySprite:
    animations = {}
    default = None

    def __init__(self, x: float, y: float, anim_name: str, frame: int = 0):
        self.x = x
        self.y = y
        self.cur_animation_name = anim_name
        self.frame = frame

    def get_cur_animation_name(self) -> str:
        return self.cur_animation_name

    def get_cur_frame(self) -> int:
        return self.frame

    def get_cur_animation(self) -> Animation:
        return self.animations[self.cur_animation_name]

    def get_sprite(self) -> pygame.Surface:
        return self.get_cur_animation()[self.frame]

    def set_animation(self, new_animation_name: str, new_frame: int):
        self.cur_animation_name = new_animation_name
        self.frame = new_frame % len(self.get_cur_animation())

    def set_position(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y


@cls_init
class PlayerSprite(EntitySprite):
    @classmethod
    def cls_init(cls):
        cls.animations = parse_config(
            './src/utility/animations/melee_animations.json')
        cls.default = 'idle'


@cls_init
class MeleeSprite(EntitySprite):
    @classmethod
    def cls_init(cls):
        cls.animations = parse_config(
            './src/utility/animations/melee_animations.json')
        cls.default = 'idle'
