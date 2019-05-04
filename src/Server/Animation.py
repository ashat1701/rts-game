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
    def __init__(self, animations, direction_binds):
        self._possible_animations = animations
        self._cur_animation_name = None
        self._cur_frame_start = None
        self._cur_frame = None
        self._direction_binds = direction_binds

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

    def get_move_animation(self, direction):
        if self._direction_binds is None:
            raise RuntimeError("Direction binds for this animation set were"
                               "not specified in config")
        return self._direction_binds[direction]


class AnimationSystem:
    def __init__(self):
        self._anim_sets = {}

    def reset_animation(self, id_, animation_name):
        if id_ not in self._anim_sets:
            self.add_entity(id_)

        self._anim_sets[id_].reset_animation(animation_name)

    def continue_or_reset(self, id_, animation_name):
        if id_ not in self._anim_sets:
            self.add_entity(id_)

        if self._anim_sets[id_].get_state()[0] != animation_name:
            self.reset_animation(id_, animation_name)

    def add_entity(self, id_):
        logging.info("AnimationSystem: Added entity {}".format(id_))
        entity = World.entity[id_]
        self._anim_sets[id_] = AnimationSet(entity.animations,
                                            entity.direction_binds)
        self._anim_sets[id_].reset_animation(entity.default_animation)

    def get_animation_state(self, id_):
        if id_ not in self._anim_sets:
            self.add_entity(id_)

        return self._anim_sets[id_].get_state()

    def continue_or_reset_move_animation(self, id_, direction):
        required_anim = self.get_move_animation(id_, direction)
        self.continue_or_reset(id_, required_anim)

    def get_move_animation(self, id_, direction):
        logging.debug("id - {} direction - {}".format(id_, direction))
        return self._anim_sets[id_].get_move_animation(direction)


def parse_config(filename: str):
    with open(filename) as f:
        config = json.load(f)

    animations = _parse_animations(config)
    direction_binds = _parse_direction_binds(config)
    return animations, direction_binds


def _parse_animations(config_obj):
    animations = {}
    for anim in config_obj:
        if anim['name'] in animations:
            raise RuntimeError("Animation {} is specified twice")

        static_anim = StaticAnimation(anim['frame_duration'],
                                      len(anim['sprites']),
                                      anim['play_once'])
        animations[anim['name']] = static_anim

    return animations


def _parse_direction_binds(config_obj):
    binds = {}
    for anim, direction in _iter_all_binds(config_obj):
        if direction in binds:
            raise RuntimeError("Animation to direction {} was binded twice"
                               .format(direction))
        binds[direction] = anim['name']

    if len(binds) != 9 and len(binds) != 0:
        raise RuntimeError("Animation has at least one direction bind in "
                           "which case all of them are required")

    return binds if len(binds) != 0 else None


def _iter_all_binds(config_obj):
    for anim in config_obj:
        for direction in anim.get('direction_binds', []):
            yield anim, tuple(direction)
