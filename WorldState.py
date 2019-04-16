import Map


class WorldState:
    def __init__(self):
        self.entity = {}
        self.enemies = set()
        self.projectiles = set()
        self.map = Map.Map()

    def get_position(self, entity_id):
        return self.entity[entity_id].get_position()

    def get_direction(self, entity_id):
        return self.entity[entity_id].get_direction()

    def get_velocity(self, entity_id):
        return self.entity[entity_id].get_velocity()

    def set_position(self, entity_id, position):
        self.entity[entity_id].set_position(position)

    def set_direction(self, entity_id, direction):
        self.entity[entity_id].set_direction(direction)

    def set_velocity(self, entity_id, velocity):
        self.entity[entity_id].set_velocity(velocity)

    def delete_entity(self, entity_id):
        self.entity.pop(entity_id, None)
        self.enemies.discard(entity_id)
        self.projectiles.discard(entity_id)


World = WorldState()
