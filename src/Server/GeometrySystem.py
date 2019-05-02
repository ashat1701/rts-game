from src.Server.WorldState import World
from src.utility.constants import *
from random import randint


class GeometrySystem:
    # @staticmethod
    # def move(entity_id):
    #     entity = World.entity[entity_id]
    #     World.map.set(*entity.get_position(), FREE_SPACE)
    #     entity.move()
    #     World.map.set(*entity.get_position(), entity_id)

    # TODO: нормальная система зрения
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

    def get_attackable_entites(self, entity_id) -> list:
        entities_id = []
        for other_entity_id in World.entity.keys():
            if self._is_attackable(World.get_position(entity_id), World.get_position(other_entity_id))\
                    and other_entity_id != entity_id:
                entities_id.append(other_entity_id)
        return entities_id

    # TODO: A*
    def generate_npc_movement(self, npc_id):
        return randint(-1, 1), randint(-1, 1)

    # Провекра пересечения хитбоксов
    @staticmethod
    def collide(box1, box2):
        return box1.colliderect(box2)

    @staticmethod
    def collide_with_wall(box):
        return not (World.map.get(box.top) != WALL and World.map.get(box.bottom) != WALL\
        and World.map.get(box.left) != WALL and World.map.get(box.right) != WALL)
