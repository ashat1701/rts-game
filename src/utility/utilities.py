import json
from src.Server.Animation import StaticAnimation
import os



def cls_init(cls):
    cls.cls_init()
    return cls


def join_paths(folder, filenames):
    return [os.path.join(folder, f) for f in filenames]
