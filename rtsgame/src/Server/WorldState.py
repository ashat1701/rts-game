from copy import deepcopy

from rtsgame.src.Server import Map
from rtsgame.src.utility.constants import *


class WorldState:
    def __init__(self, game_mode='Singleplayer'):
        self.game_mode = game_mode
        self.entity = {}
        self.movable_entities = set()
        self.enemies = set()
        self.projectiles = set()
        self.dead_entities = []
        self.map = Map.Map(width=WIDTH, height=HEIGHT, max_rooms=ROOMS,
                           min_room_len=MIN_ROOM_LEN,
                           max_room_len=MAX_ROOM_LEN,
                           random_connections=RANDOM_CONNECTIONS)
        self.first_player_glare = deepcopy(self.map.level)
        self.second_player_glare = deepcopy(self.map.level)
        self.first_player_id = 0
        self.second_player_id = 1

    def get_game_mode(self):
        return self.game_mode

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode
        if game_mode == 'Singleplayer':
            self.player_dead = [False]
        else:
            self.player_dead = [False, False]

    def get_first_player_id(self):
        return self.first_player_id

    def get_second_player_id(self):
        return self.second_player_id

    def get_position(self, entity_id):
        return (
            self.get_box(entity_id).centerx, self.get_box(entity_id).centery)

    def get_direction(self, entity_id):
        return self.entity[entity_id].get_direction()

    def get_velocity(self, entity_id):
        return self.entity[entity_id].get_velocity()

    def get_damage(self, entity_id):
        return self.entity[entity_id].get_damage()

    def get_health(self, entity_id):
        return self.entity[entity_id].get_health()

    def get_box(self, entity_id):
        return self.entity[entity_id].get_box()

    def get_last_attack(self, entity_id):
        return self.entity[entity_id].get_last_attack()

    def get_attack_reload(self, entity_id):
        return self.entity[entity_id].get_attack_reload()

    def set_last_attack(self, entity_id, last_attack):
        self.entity[entity_id].set_last_attack(last_attack)

    def set_attack_reload(self, entity_id, attack_reload):
        self.entity[entity_id].set_attack_reload(attack_reload)

    def set_box(self, entity_id, box):
        self.entity[entity_id].set_box(box)

    def set_position(self, entity_id, position):
        self.entity[entity_id].set_position(position)

    def set_direction(self, entity_id, direction):
        self.entity[entity_id].set_direction(direction)

    def set_velocity(self, entity_id, velocity):
        self.entity[entity_id].set_velocity(velocity)

    def set_damage(self, entity_id, damage):
        self.entity[entity_id].set_damage(damage)

    def set_health(self, entity_id, health):
        self.entity[entity_id].set_health(health)

    def delete_entity(self, entity_id):
        self.movable_entities.discard(entity_id)
        del self.entity[entity_id]
        self.enemies.discard(entity_id)
        self.projectiles.discard(entity_id)


world = WorldState()

def recreate_world():
    global world
    world = WorldState()