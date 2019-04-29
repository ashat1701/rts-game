import Entity
from WorldState import World
from random import randint
from constants import *
from Entity import MeleeEnemy


class SpawnSystem:
    def __init__(self):
        self._current_id = -1
        self._enemy_types = []

        # TODO make player spawner
        self.create_player()


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
        World.movable_entities.add(self._current_id)
        World.enemies.add(self._current_id)

    def create_player(self):
        World.entity[0] = MeleeEnemy().set_damage(10).set_velocity(10)\
            .set_damage(0).set_direction((0, 0)).set_position((0, 0)).set_health(10).set_id(self._current_id)

    def create_item(self):
        pass

def generate_random_direction():
    return 0, 0


def generate_enemy_damage():
    return 0


def generate_enemy_health():
    return 0
