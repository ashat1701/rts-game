import json
from Animation import Animation

def cls_init(cls):
    cls.cls_init()
    return cls


def parse_animation_config(filename: str):
    with open(filename) as f:
        config = json.load(f)

    animations = {anim['name']: Animation(anim['duration'],
                                          len(anim['sprites']),
                                          anim['play_once'])
                  for anim in config}

    return animations
