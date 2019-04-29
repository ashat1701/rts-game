from abc import ABCMeta, abstractmethod
import pygame
from resources import Animation, get_paths
from typing import Tuple


def class_init(class_):
    class_.__cls_init__()
    return class_


class SpriteEntity:
    animations = {}

    def __init__(self, x: float, y: float, name: str, frame: int):
        self.x = x
        self.y = y
        self.cur_animation_name = name
        self.frame = frame

    def get_cur_animation_name(self) -> str:
        return self.cur_animation_name

    def get_cur_frame(self) -> int:
        return self.frame

    def get_cur_animation(self) -> Animation:
        return self.animations[self.cur_animation_name]

    def get_sprite(self) -> pygame.Surface:
        return self.get_cur_animation()[self.frame]

    def set_sprite(self, new_animation_name: str, new_frame: int):
        self.cur_animation_name = new_animation_name
        self.frame = new_frame % len(self.get_cur_animation())

    def set_cords(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y

    def get_coords(self) -> Tuple[float, float]:
        return self.x, self.y


@class_init
class PlayerSprite(SpriteEntity):
    @classmethod
    def __cls_init__(cls):
        idle_anim = Animation(get_paths('./Sprites/Player/Axe/Defence0/',
                                        ['Player_Idle_Axe_Defence0_0.png',
                                         'Player_Idle_Axe_Defence0_1.png',
                                         'Player_Idle_Axe_Defence0_2.png',
                                         'Player_Idle_Axe_Defence0_3.png']))
        cls.animations['idle'] = idle_anim

        run_anim = Animation(get_paths('./Sprites/Player/Axe/Defence0/',
                                        ['Player_Walk_Axe_Defence0_0.png',
                                         'Player_Walk_Axe_Defence0_1.png',
                                         'Player_Walk_Axe_Defence0_2.png',
                                         'Player_Walk_Axe_Defence0_3.png']))
        cls.animations['walk'] = run_anim


@class_init
class MeleeSprite(SpriteEntity):
    @classmethod
    def __cls_init__(cls):
        idle_anim = Animation(get_paths('./Sprites/Player/Special/',
                                        ['Player_Idle_Special_0.png',
                                         'Player_Idle_Special_1.png',
                                         'Player_Idle_Special_2.png',
                                         'Player_Idle_Special_3.png']))
        cls.animations['idle'] = idle_anim

        run_anim = Animation(get_paths('./Sprites/Player/Special/',
                                        ['Player_Walk_Special_0.png',
                                         'Player_Walk_Special_1.png',
                                         'Player_Walk_Special_2.png',
                                         'Player_Walk_Special_3.png']))
        cls.animations['run'] = run_anim
