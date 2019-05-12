import json
import os

import pygame

from rtsgame.src.Client.Animation import parse_descriptions
from rtsgame.src.Client.Sprite import Sprite
from rtsgame.src.utility.constants import PIXEL_SCALE, MAP_SCALE
from rtsgame.src.utility.utilities import Vector


class EntitySpriteManager:
    _animations = {}

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Sprite Manager is static class")

    @classmethod
    def register_animations(cls, entity_type, animations):
        if cls.has_type(entity_type):
            raise RuntimeError("Entity_type {}"
                               "is already registered")

        cls._animations[entity_type] = animations

    @classmethod
    def get_sprite(cls, entity_type, animation_name, frame):
        if not cls.has_animation(entity_type, animation_name):
            raise RuntimeError("Entity {} doesn't exist or doesn't have "
                               "animation {}"
                               .format(entity_type, animation_name))
        return cls._animations[entity_type][animation_name][frame]

    @classmethod
    def get_offset(cls, entity_type, animation_name):
        if not cls.has_animation(entity_type, animation_name):
            raise RuntimeError("Entity {} doesn't exist or doesn't have "
                               "animation {}"
                               .format(entity_type, animation_name))
        return cls._animations[entity_type][animation_name].offset

    @classmethod
    def has_type(cls, entity_type):
        return entity_type in cls._animations

    @classmethod
    def has_animation(cls, entity_type, animation_name):
        return (cls.has_type(entity_type) and
                animation_name in cls._animations[entity_type])

    @classmethod
    def load_entity_config(cls, filename):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "../../" + filename)) as file:
            config = json.load(file)

        all_animations = parse_descriptions(config['move'])
        all_animations.update(parse_descriptions(config['attack']))
        cls.register_animations(config['entity_type'], all_animations)


class EntitySprite(Sprite):
    def __init__(self, info, debug=False):
        super().__init__()
        self.debug = debug
        self.info = info
        self.x = info[0][0] / MAP_SCALE * PIXEL_SCALE
        self.y = info[0][1] / MAP_SCALE * PIXEL_SCALE
        self.box = None

    @property
    def type(self):
        return self.info[1]

    @property
    def animation_name(self):
        return self.info[2]

    @property
    def frame(self):
        return self.info[3]

    @property
    def position(self):
        return Vector(self.x, self.y)

    @property
    def sprite(self):
        return EntitySpriteManager.get_sprite(self.type, self.animation_name,
                                              self.frame)

    @property
    def health(self):
        return self.info[4][0]

    @property
    def offset(self):
        return EntitySpriteManager.get_offset(self.type, self.animation_name)

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        if self.debug:
            pygame.draw.rect(surface, (255, 255, 255),
                             (
                                 abs_position, (PIXEL_SCALE / 2, PIXEL_SCALE / 2)))
        surface.blit(self.sprite, abs_position - self.offset)

        super().draw(surface, abs_position)
