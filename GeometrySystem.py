from WorldState import World
from constants import *
from random import randint


class GeometrySystem:
    def move(self, entity_id):
        entity = World.entity[entity_id]
        World.map.set(*entity.get_position(), FREE_SPACE)
        entity.move()
        World.map.set(*entity.get_position(), entity_id)

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
