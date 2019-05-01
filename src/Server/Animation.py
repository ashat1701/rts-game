import time
import json
import logging
from src.Server.WorldState import World


class StaticAnimation:
    def __init__(self, duration: int, frame_num: int, play_once: bool):
        self.duration = duration
        self.frame_num = frame_num
        self.play_once = play_once


class AnimationSet:
    def __init__(self, animations):
        self._possible_animations = animations
        self._cur_animation_name = None
        self._cur_frame_start = None
        self._cur_frame = None

    def get_state(self):
        time_delta = int(time.time() * 1000) - self._cur_frame_start
        frames_skip = time_delta // self.cur_animation.duration

        if frames_skip > 0:
            self.set_frame(self._cur_frame + frames_skip)

        return self._cur_animation_name, self._cur_frame

    def set_frame(self, new_frame):
        if new_frame > self.cur_animation.frame_num:
            if self.cur_animation.play_once:
                new_frame = self.cur_animation.frame_num - 1
            else:
                new_frame %= self.cur_animation.frame_num

        self._cur_frame_start = int(time.time() * 1000)
        self._cur_frame = new_frame

    def reset_animation(self, animation_name):
        self._cur_animation_name = animation_name
        self.set_frame(0)

    @property
    def cur_animation(self):
        return self._possible_animations[self._cur_animation_name]


class AnimationSystem:
    def __init__(self):
        self.anim_sets = {}

    def reset_animation(self, id_, animation_name):
        if id_ not in self.anim_sets:
            self.add_entity(id_)

        self.anim_sets[id_].reset_animation(animation_name)

    def continue_or_reset(self, id_, animation_name):
        if id_ not in self.anim_sets:
            self.add_entity(id_)

        if self.anim_sets[id_].get_state()[0] != animation_name:
            self.reset_animation(id_, animation_name)

    def add_entity(self, id_):
        logging.info("AnimationSystem: Added entity {}".format(id_))
        entity = World.entity[id_]
        self.anim_sets[id_] = AnimationSet(entity.animations)
        self.anim_sets[id_].reset_animation(entity.default_animation)

    def get_animation_state(self, id_):
        if id_ not in self.anim_sets:
            self.add_entity(id_)

        return self.anim_sets[id_].get_state()


def parse_config(filename: str):
    with open(filename) as f:
        config = json.load(f)

    animations = {anim['name']: StaticAnimation(anim['frame_duration'],
                                                len(anim['sprites']),
                                                anim['play_once'])
                  for anim in config}

    return animations
