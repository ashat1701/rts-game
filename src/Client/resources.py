import pygame
import logging
import os
from client_config import *
import json


class SpriteSheet(object):
    def __init__(self, filename: str, sprite_size: int = SPRITESHEET_SIZE,
                 sprite_margin: int = SPRITESHEET_MARGIN,
                 scale: int = SCALE_FACTOR):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            x, y = self.sheet.get_size()
            self.sheet = pygame.transform.scale(self.sheet,
                                                (x * scale, y * scale))
        except pygame.error as error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(error)

        self.size = sprite_size * scale
        self.margin = sprite_margin * scale
        self.filename = filename
        self.scale = scale

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None) -> pygame.Surface:
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def get_sprite(self, row: int, column: int) -> pygame.Surface:
        x, y = self.get_sprite_coords(row, column)
        logging.debug("Returned Spite at coordinates {} from {}"
                      .format((x, y), self.filename))

        return self.image_at((x, y, self.size, self.size))

    def get_sprite_coords(self, row: int, column: int):
        x = column * (self.size + self.margin)
        y = row * (self.size + self.margin)
        return x, y


class Sprite:
    def __init__(self, spritesheet: SpriteSheet, row: int, column: int):
        self.image = spritesheet.get_sprite(row, column)

    def get_sprite(self) -> pygame.Surface:
        return self.image


class Animation:
    def __init__(self, filenames, scale=SCALE_FACTOR):
        images = [pygame.image.load(f) for f in filenames]
        self.images = [pygame.transform.scale(img, (
        img.get_height() * scale, img.get_width() * scale))
                       for img in images]

    def __getitem__(self, item: int) -> pygame.Surface:
        return self.images[item]

    def __len__(self):
        return len(self.images)


def parse_animation_config(filename: str):
    with open(filename) as f:
        config = json.load(f)
    print(config[0]['folder'])
    animations = {
    anim['name']: Animation(get_paths(anim['folder'], anim['sprites']))
    for anim in config}

    return animations


def get_paths(folder, filenames):
    return [os.path.join(folder, f) for f in filenames]
