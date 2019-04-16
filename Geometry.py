from WorldState import World
from constants import *
from random import randint


class Geometry:
    # TODO: hit registration (hitbox intersection)
    def move(self, entity_id):
        x, y = World.get_position(entity_id)
        dx, dy = [i * World.get_velocity(entity_id) for i in World.get_direction(entity_id)]
        World.map.set(x + dx, y + dy, entity_id)
        World.map.set(x, y, FREE_SPACE)
        World.set_position[entity_id] = (x + dx, y + dy)

    @staticmethod
    def _is_visible(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5 < VISION_RANGE

    @staticmethod
    def _is_attackable(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5 < ATTACK_RANGE

    def get_visible_entities(self, entity_id) -> list:
        entities_id = []
        for other_entity_id in World.entity.keys():
            if self._is_visible(World.get_position(entity_id), World.get_position(other_entity_id)):
                entities_id.append(other_entity_id)
        return entities_id

    # TODO: A*
    def generate_npc_movement(self, npc_id):
        return randint(-1, 1), randint(-1, 1)

    # May be World.moveable_entities?
    def move_all_npc(self):
        for entity_id in World.entity.keys():
            self.move(entity_id)

a = {1: '1'}

print(1 in a)