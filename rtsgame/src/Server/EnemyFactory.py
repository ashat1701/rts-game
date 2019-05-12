import json
import os
from random import randint

from pygame import Rect

from .Entity import MeleeEnemy
from ..utility.constants import *


class EnemyFactory:
    def __init__(self):
        pass

    def generate_enemy(self):
        raise NotImplementedError


class MeleeEnemyFactory(EnemyFactory):
    def __init__(self):
        super().__init__()
        self.box_width = ENEMY_BOX_SIZE
        self.box_height = ENEMY_BOX_SIZE
        self.min_health = 10
        self.max_health = self.min_health * 2
        self.damage = 2
        self.id = 2

    def generate_enemy(self):
        current_id = self.id
        self.id += 1
        box = generate_box(self.box_width, self.box_height)
        damage = self.damage
        health = generate_enemy_health(self.min_health, self.max_health)
        direction = generate_random_direction()
        print("BOX {} health {} direction {} id {}".format(box, health, direction, current_id))
        return MeleeEnemy().set_id(current_id).set_box(box).set_damage(damage) \
            .set_health(health).set_direction(direction).set_attack_reload(
            ATTACK_RELOAD).set_velocity(ENEMY_VELOCITY)

    def load_difficulty_from_file(self, name):
        dirname = os.path.dirname(__file__)
        obj = json.load(open(os.path.join(dirname, "../../src/utility/difficulties/{}.json".format(name))))
        self.box_width = obj["enemies"][0]["box_width"]
        self.box_height = obj["enemies"][0]["box_height"]
        self.min_health = obj["enemies"][0]["min_health"]
        self.max_health = obj["enemies"][0]["max_health"]


def generate_random_direction():
    return 1, 0


def generate_enemy_damage():
    return 10


def generate_enemy_health(min_health, max_health):
    return randint(min_health, max_health + 1)


def generate_box(width, height):
    return Rect(0, 0, width, height)
