from math import sin, cos, inf

from rtsgame.src.Server.Entity import PlayerEntity, Enemy
from rtsgame.src.Server.WorldState import world
from rtsgame.src.utility.constants import *


class GeometrySystem:

    def get_visible_tiles(self, entity_id):
        # Обновлять glare для правильного игрока
        glare_map = None
        visible_tiles = []
        if entity_id == world.first_player_id:
            glare_map = world.first_player_glare
        if entity_id == world.second_player_id:
            glare_map = world.second_player_id

        for i in range(360):
            deg = i * 3.1415 / 180
            x0 = world.get_box(entity_id).centerx
            y0 = world.get_box(entity_id).centery
            x = round(cos(deg) * VISION_RANGE) + world.get_box(
                entity_id).centerx
            y = round(sin(deg) * VISION_RANGE) + world.get_box(
                entity_id).centery

            diag_dist = max(abs(x - x0), abs(y - y0))

            for j in range(diag_dist):
                tx = round(x0 + (j / diag_dist) * (x - x0))
                ty = round(y0 + (j / diag_dist) * (y - y0))

                if (tx < 0 or tx >= world.map.width * MAP_SCALE) or (
                        ty < 0 or ty >= world.map.height * MAP_SCALE):
                    break
                if world.map.level[tx][ty] == WALL:
                    visible_tiles.append((tx, ty))
                    break
                visible_tiles.append((tx, ty))
                if glare_map is not None:
                    glare_map[tx][ty] = 1
        return visible_tiles

    @staticmethod
    def get_squared_distance(entity_id1, entity_id2):
        return (world.get_box(entity_id1).centerx - world.get_box(entity_id2).centerx) ** 2 + \
               (world.get_box(entity_id1).centery - world.get_box(entity_id2).centery) ** 2

    # TODO: нормальная система зрения
    @staticmethod
    def _is_visible(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (
                position1[1] - position2[1]) ** 2) ** 0.5 < VISION_RANGE

    @staticmethod
    def _is_attackable(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (
                position1[1] - position2[1]) ** 2) ** 0.5 < ATTACK_RANGE

    def get_visible_entities(self, entity_id) -> list:
        entities_id = []
        for other_entity_id in world.entity.keys():
            if self._is_visible(world.get_position(entity_id),
                                world.get_position(other_entity_id)):
                entities_id.append(other_entity_id)
        return entities_id

    def get_attackable_entites(self, entity_id) -> list:
        entities_id = []
        if isinstance(world.entity[entity_id], PlayerEntity):
            EnemyClass = Enemy
        if isinstance(world.entity[entity_id], Enemy):
            EnemyClass = PlayerEntity

        for other_entity_id in world.entity.keys():
            if isinstance(world.entity[other_entity_id], EnemyClass):
                if self._is_attackable(world.get_position(entity_id), world.get_position(other_entity_id)) \
                        and other_entity_id != entity_id:
                    entities_id.append(other_entity_id)
        return entities_id

    def generate_npc_movement(self, npc_id):
        if world.entity[npc_id].get_aim() is None:
            return (0, 0)
        target = world.entity[npc_id].get_aim()
        current = world.get_position(npc_id)
        directions = [(0, 0), (0, 1), (1, 1), (1, 0), (-1, 0), (-1, -1), (0, -1), (1, -1), (-1, 1)]
        ans = (0, 0)
        min_dist = 10 ** 10
        for direction in directions:
            new_cur = (current[0] + direction[0], current[1] + direction[1])
            if ((new_cur[0] - target[0]) ** 2 + (new_cur[1] - target[1]) ** 2) < min_dist:
                min_dist = (new_cur[0] - target[0]) ** 2 + (new_cur[1] - target[1]) ** 2
                ans = direction
        return ans

    # Провекра пересечения хитбоксов
    @staticmethod
    def collide(box1, box2):
        return box1.colliderect(box2)

    @staticmethod
    def collide_with_wall(box):  # Саша проверь
        non_passable_textures = {WALL, STONE}
        return world.map.get(
            *box.topleft) in non_passable_textures or world.map.get(
            *box.topright) \
               in non_passable_textures or world.map.get(
            *box.bottomleft) in non_passable_textures or \
               world.map.get(*box.bottomright) in non_passable_textures

    def find_aim(self, entity_id):
        if world.game_mode == "Multiplayer":
            if not world.player_dead[world.get_first_player_id()]:
                dist_to_first_player = self.get_squared_distance(entity_id, world.get_first_player_id())
            else:
                dist_to_first_player = inf

            if not world.player_dead[world.get_second_player_id()]:
                dist_to_second_player = self.get_squared_distance(entity_id, world.get_second_player_id())
            else:
                dist_to_second_player = inf

            dist_to_aim = min(dist_to_first_player, dist_to_second_player)

            if dist_to_first_player < dist_to_second_player:
                probable_aim = world.get_box(world.get_first_player_id()).center

            else:
                probable_aim = world.get_box(world.get_second_player_id()).center

            if dist_to_aim < VISION_RANGE ** 2:
                world.entity[entity_id].set_aim(probable_aim)
        if world.game_mode == "Singleplayer":
            dist_to_first_player = self.get_squared_distance(entity_id, world.get_first_player_id())
            if dist_to_first_player < VISION_RANGE ** 2:
                world.entity[entity_id].set_aim(world.get_box(world.get_first_player_id()).center)
