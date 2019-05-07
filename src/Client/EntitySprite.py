import json

import pygame

from src.Client.UI.Widget import Widget
from src.utility.utilities import Vector
from src.utility.utilities import load_sprites, join_paths


class EntitySpriteManager:
    _animations = {}

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Sprite Manager is static class")

    @classmethod
    def register_animation(cls, entity_type, animation_name, sprites):
        if not cls.has_type(entity_type):
            cls._animations[entity_type] = {}

        if cls.has_animation(entity_type, animation_name):
            raise RuntimeError("Animation {} for entity_type {}"
                               "is already registered")

        cls._animations[entity_type][animation_name] = sprites

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
    def load_entity_config(cls, config, entity_type=None):
        if isinstance(config, str):
            with open(config) as file:
                config = json.load(file)

        if entity_type is not None:
            if not isinstance(config, list):
                raise RuntimeError("If you specify name in load config, then"
                                   "config has to be json list.")
            animation_descriptions = config
        else:
            if not isinstance(config, dict):
                raise RuntimeError("if you don't specify name in "
                                   "load_entity_config then config file has to"
                                   " be dict with ")
            entity_type = config['entity_type']
            animation_descriptions = config['animations']

        for description in animation_descriptions:
            sprite_paths = join_paths(description['folder'],
                                      description['sprites'])
            sprites = load_sprites(sprite_paths)
            cls.register_animation(entity_type, description['name'], sprites)


def _load_animation(description):
    sprite_files = join_paths(description['folder'], description['sprites'])
    return description['name'], load_sprites(sprite_files)


class EntitySprite(Widget):
    def __init__(self, info):
        super().__init__()
        self.info = info

    @property
    def id(self):
        return self.info[0]

    @property
    def x(self):
        return self.info[0]

    @property
    def y(self):
        return self.info[0]

    @property
    def type(self):
        return self.info[0]

    @property
    def animation_name(self):
        return self.info[0]

    @property
    def frame(self):
        return self.info[0]

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
