from src import Map


class WorldState:
    def __init__(self):
        self.entity = {}
        self.movable_entities = set()
        self.enemies = set()
        self.projectiles = set()
        self.map = Map.Map(width=100, height=100, max_rooms=10, min_room_len=5, max_room_len=10, random_connections=5)
        self.first_player_id = 0
        self.second_player_id = 1
        self.first_player_moving = False
        self.second_player_moving = False

    def get_first_player_id(self):
        return self.first_player_id

    def get_second_player_id(self):
        return self.second_player_id

    def get_position(self, entity_id):
        return self.entity[entity_id].get_position()

    def get_direction(self, entity_id):
        return self.entity[entity_id].get_direction()

    def get_velocity(self, entity_id):
        return self.entity[entity_id].get_velocity()

    def get_damage(self, entity_id):
        return self.entity[entity_id].get_damage()

    def get_health(self, entity_id):
        return self.entity[entity_id].get_health()

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
        self.entity.pop(entity_id, None)
        self.enemies.discard(entity_id)
        self.projectiles.discard(entity_id)


World = WorldState()
