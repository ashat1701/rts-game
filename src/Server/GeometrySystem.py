from src.Server.WorldState import World
from src.utility.constants import *
from random import randint
from math import sin, cos


class GeometrySystem:
    # @staticmethod
    # def move(entity_id):
    #     entity = World.entity[entity_id]
    #     World.map.set(*entity.get_position(), FREE_SPACE)
    #     entity.move()
    #     World.map.set(*entity.get_position(), entity_id)
    
    def get_visible_tiles(self, entity_id):
        # Обновлять glare для правильного игрока
        glare_map = None
        visible_tiles = []
        if entity_id == World.first_player_id:
            glare_map = World.first_player_glare
        if entity_id == World.second_player_id:
            glare_map = World.second_player_id

        for i in range(360):
            deg = i * 3.1415 / 180
            x0 = World.get_box(entity_id).centerx / MAP_SCALE
            y0 = World.get_box(entity_id).centery / MAP_SCALE
            x = round(cos(deg) * VISION_RANGE) + World.get_box(entity_id).centerx // MAP_SCALE
            y = round(sin(deg) * VISION_RANGE) + World.get_box(entity_id).centery // MAP_SCALE

            diag_dist = max(abs(x - x0), abs(y - y0))

            for j in range(diag_dist):
                tx = round(x0 + (j / diag_dist) * (x - x0))
                ty = round(y0 + (j / diag_dist) * (y - y0))

                if (tx < 0 or tx >= World.map.width) or (ty < 0 or ty >= World.map.height):
                    break
                if World.map.level[tx][ty] == WALL:
                    visible_tiles.append((tx, ty))
                    break
                visible_tiles.append((tx, ty))
                if glare_map is not None:
                    glare_map[tx][ty] = 1
        return visible_tiles

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
    def collide_with_wall(box): # Саша проверь
        non_passable_textures = {WALL, STONE}
        return World.map.get(*box.topleft) in non_passable_textures or World.map.get(*box.topright) \
            in non_passable_textures or World.map.get(*box.bottomleft) in non_passable_textures or \
               World.map.get(*box.bottomright) in non_passable_textures