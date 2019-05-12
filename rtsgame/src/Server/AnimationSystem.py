import json
import logging
import time

from rtsgame.src.Server.WorldState import world


class StaticAnimation:
    def __init__(self, duration: int, frame_num: int, play_once: bool):
        self.duration = duration
        self.frame_num = frame_num
        self.play_once = play_once


class AnimationSet:
    def __init__(self, animations, move_binds, attack_binds, anim):
        self._possible_animations = animations
        self._cur_animation_name = None
        self._cur_frame_start = None
        self._cur_frame = None
        self.reset_animation(anim)
        self._move_binds = move_binds
        self._attack_binds = attack_binds

    def get_state(self):
        time_delta = int(time.time() * 1000) - self._cur_frame_start
        frames_skip = time_delta // self.cur_animation.duration

        if frames_skip > 0:
            self.set_frame(self._cur_frame + frames_skip)

        return self._cur_animation_name, self._cur_frame

    def set_frame(self, new_frame):
        if new_frame >= self.cur_animation.frame_num:
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
        if self._move_binds is None:
            raise RuntimeError("Direction binds for this animation set were"
                               "not specified in config")
        return self._move_binds[direction]

    def get_attack_animation(self, direction):
        if self._attack_binds is None:
            raise RuntimeError("Direction binds for this animation set were"
                               "not specified in config")
        return self._attack_binds[direction]


class AnimationSetFactory:
    def __init__(self):
        self._set_inits = {}

    def register(self, entity_type, animations, move_binds, attack_binds,
                 default_animation):
        if entity_type in self._set_inits:
            raise RuntimeError("{} Already registered for animation set"
                               "factory".format(entity_type))
        self._set_inits[entity_type] = (animations, move_binds, attack_binds,
                                        default_animation)

    def get_animation_set(self, entity_type):
        animation_set = AnimationSet(*self._set_inits[entity_type])
        return animation_set


class AnimationSystem:
    def __init__(self):
        self._anim_sets = {}
        self.factory = AnimationSetFactory()

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
        entity_type = world.entity[id_].get_type()

        self._anim_sets[id_] = self.factory.get_animation_set(entity_type)

    def remove_entity(self, id_):
        del self._anim_sets[id_]

    def get_animation_state(self, id_):
        if id_ not in self._anim_sets:
            self.add_entity(id_)
        return self._anim_sets[id_].get_state()

    def continue_or_reset_move_animation(self, id_, direction):
        required_anim = self.get_move_animation(id_, direction)
        self.continue_or_reset(id_, required_anim)

    def get_move_animation(self, id_, direction):
        logging.debug("id - {} direction - {}".format(id_, direction))
        if id_ not in self._anim_sets:
            self.add_entity(id_)
        return self._anim_sets[id_].get_move_animation(direction)

    def get_attack_animation(self, id_, direction):
        if id_ not in self._anim_sets:
            self.add_entity(id_)
        return self._anim_sets[id_].get_attack_animation(direction)

    def load_entity_config(self, file):
        with open(file) as f:
            config = json.load(f)

        all_animations, move_binds = parse_animation_descriptions(
            config['move'])
        attack_animations, attack_binds = parse_animation_descriptions(
            config['attack'])

        all_animations.update(attack_animations)
        self.factory.register(config['entity_type'],
                              all_animations,
                              move_binds,
                              attack_binds,
                              config['default'])


def parse_animation_descriptions(config):
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
