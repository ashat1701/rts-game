import pygame
import json
from src.utility.client_config import *
from src.utility.utilities import join_paths


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


def parse_config(filename: str):
    with open(filename) as f:
        config = json.load(f)
    print(config[0]['folder'])
    animations = {
        anim['name']: Animation(join_paths(anim['folder'], anim['sprites']))
        for anim in config}

    return animations
