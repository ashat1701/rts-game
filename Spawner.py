import Entity
from WorldState import World
from random import randint
from constants import *



class Spawner:
    def __init__(self):
        self._current_id = -1
        self._enemy_types = []

    def add_enemy_type(self, enemy_type: Entity.Enemy):
        self._enemy_types.append(enemy_type)

    def create_enemy(self, position=None):
        enemy_type = randint(0, len(self._enemy_types) - 1)
        self._current_id += 1
        damage = generate_enemy_damage()
        health = generate_enemy_health()
        direction = generate_random_direction()
        entity = enemy_type().set_damage(damage).set_velocity(ENEMY_VELOCITY)\
            .set_damage(damage).set_direction(direction).set_position(position).set_health(health).set.set_id(self._current_id)
        World.entity[self._current_id] = entity
        World.enemies.add(self._current_id)

    def create_player(self):
        pass

    def create_item(self):
        pass

def generate_random_direction():
    return 0, 0


def generate_enemy_damage():
    return 0


def generate_enemy_health():
    return 0
