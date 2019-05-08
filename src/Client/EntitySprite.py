import json

import pygame
import os
from src.Client.UI.Widget import Widget
from src.utility.utilities import Vector
from src.utility.utilities import load_sprites, join_paths
from src.Client.Animation import Animation, parse_descriptions


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
    def has_type(cls, entity_type):
        return entity_type in cls._animations

    @classmethod
    def has_animation(cls, entity_type, animation_name):
        return (cls.has_type(entity_type) and
                animation_name in cls._animations[entity_type])

    @classmethod
    def load_entity_config(cls, filename):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.." + filename)) as file:
            config = json.load(file)

        cls.register_animations(config['entity_type'],
                                parse_descriptions(config['animations']))


class EntitySprite(Widget):
    def __init__(self, info):
        super().__init__()
        self.info = info

    @property
    def id(self):
        return self.info[0]

    @property
    def x(self):
        return self.info[0][0]

    @property
    def y(self):
        return self.info[0][1]

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

    def draw(self, surface: pygame.Surface, abs_position: Vector):
        super().draw(surface, abs_position)

        surface.blit(self.sprite, abs_position)
