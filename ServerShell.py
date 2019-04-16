from constants import *
import queue
import Server
import logging
import time
import random
from ActionBuilder import ActionBuilder
import Map
import Spawner


class World:
    def __init__(self):
        self.server = Server.SafeServer()
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()
        # Systems
        self.map = Map.Map()
        self.spawner = Spawner.Spawner()

        self._entity = {}
        self._enemy = set()
        self._projectiles = set()

        self.first_player = self.create_entity(position=(1, 1), health=100, damage=50, velocity=(1, 1))
        self.second_player = self.create_entity(position=(MAX_X - 2, MAX_Y - 2))
        self.test_enemy = self.create_entity(position=(MAX_X // 2, MAX_Y // 2), health=100)
        self.add_enemy(self.test_enemy)

        self.player_moving = False

    def create_entity(self, position=None, health=None, damage=None, velocity=None, direction=None) -> int:
        self._current_id += 1
        if position is not None:
            self._position[self._current_id] = position
        if health is not None:
            self._health[self._current_id] = health
        if damage is not None:
            self._damage[self._current_id] = damage
        if velocity is not None:
            self._velocity[self._current_id] = velocity
        if direction is not None:
            self._direction[self._current_id] = direction
        return self._current_id

    def add_enemy(self, entity_id):
        self._enemy.add(entity_id)

    def get_position(self, entity_id):
        return self._position[entity_id]

    # TODO: hit registration (hitbox intersection)
    def move(self, entity_id, dx, dy):
        x = self._position[entity_id][0]
        y = self._position[entity_id][1]
        self._direction[entity_id] = (dx // abs(dx) if dx != 0 else 0, dy // abs(dy) if dy != 0 else 0)
        if entity_id in self._projectiles:
            if self.map.get(x + dx, y + dy) == WALL:
                self.delete_entity(entity_id)
            elif self.map.get(x + dx, y + dy) != FREE_SPACE:
                hit_entity = self.map.get(x + dx, y + dy)
                self._health[hit_entity] -= self._damage[entity_id]
                self.delete_entity(entity_id)
        if self.map.get(x + dx, y + dy) == FREE_SPACE:
            self.map.set(x + dx, y + dy, entity_id)
            self.map.set(x, y, FREE_SPACE)
            self._position[entity_id] = (x + dx, y + dy)

    def get_attackable_entities(self, entity_id):
        entities_id = []
        for other_entity_id, entity_position in self._position.items():
            if self._is_attackable(self._position[entity_id],
                                self._position[other_entity_id]) and entity_id != other_entity_id:
                entities_id.append(other_entity_id)
        return entities_id

    # TODO: A*
    def generate_npc_movement(self, npc_id):
        return random.randint(-1, 1), random.randint(-1, 1)

    def move_all_npc(self):
        for enemy in self._enemy:
            change_x, change_y = self.generate_npc_movement(enemy)
            self.move(enemy, change_x, change_y)
        for projectile in self._projectiles:
            change_x, change_y = self._direction[projectile][0] * self._velocity[projectile],\
                                 self._direction[projectile][1] * self._velocity[projectile]
            self.move(projectile, change_x, change_y)

    # TODO: analyze walls
    @staticmethod
    def _is_visible(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5 < VISION_RANGE

    @staticmethod
    def _is_attackable(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5 < ATTACK_RANGE

    def attack(self, entity_id):
        attackable_entities = self.get_attackable_entities(entity_id)
        for other_entity_id in attackable_entities:
            self._health[other_entity_id] -= self._damage[entity_id]
            if self._health[other_entity_id] < 0:
                self.delete_entity(other_entity_id)

    def shoot(self, entity_id):
        self.create_entity(position=self._position[entity_id], damage=PROJECTILE_DAMAGE, velocity=PROJECTILE_VELOCITY,
                           direction=self._direction[entity_id])

    def delete_entity(self, entity_id):
        self._position.pop(entity_id, None)
        self._health.pop(entity_id, None)
        self._damage.pop(entity_id, None)
        self._velocity.pop(entity_id, None)
        self._enemy.remove(entity_id)

    def get_visible_entities(self, entity_id) -> list:
        entities_id = []
        for other_entity_id, entity_position in self._position.items():
            if self._is_visible(self._position[entity_id],
                                self._position[other_entity_id]) and entity_id != other_entity_id:
                entities_id.append(other_entity_id)
        return entities_id

    def update(self):
        while not self.server.action_queue.empty():
            player_id, current_action = self.server.action_queue.get()
            if current_action == "STOP":
                self.player_moving = False
            if current_action.starts_with("MOVE"):
                self.player_moving = True
                if current_action == "MOVE_UP":
                    self._direction[self.first_player] = (0, 1)
                if current_action == "MOVE_DOWN":
                    self._direction[self.first_player] = (0, -1)
                if current_action == "MOVE_LEFT":
                    self._direction[self.first_player] = (-1, 0)
                if current_action == "MOVE_RIGHT":
                    self._direction[self.first_player] = (1, 0)
            if current_action == "ATTACK":
                self.attack(player_id)
            if self.player_moving is True:
                self.move(self.first_player, self._direction[self.first_player][0] * self._velocity[self.first_player],
                          self._direction[self.first_player][1] * self._velocity[self.first_player])

        self.move_all_npc()

    def send_information(self):
        entities_to_draw = []

        if self.player_moving is True:
            entities_to_draw.append(ActionBuilder().set_x(self._position[self.first_player][0])
                                    .set_y(self._position[self.first_player][1]).set_type("PLAYER").get_action())
        visible_entities = self.get_visible_entities(self.first_player)
        for visible_entity in visible_entities:
            if visible_entity in self._enemy:
                entities_to_draw.append(ActionBuilder().set_x(self._position[visible_entity][0])
                                        .set_y(self._position[visible_entity][1]).set_type("ENEMY").get_action())
            elif visible_entity in self._projectiles:
                entities_to_draw.append(ActionBuilder().set_x(self._position[visible_entity][0])
                                        .set_y(self._position[visible_entity][1]).set_type("PROJECTILE").get_action())
        self.server.send_obj_to_player(entities_to_draw, self.first_player)


if __name__ == '__main__':
    world = World()
    while True:
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        world.update()
        world.send_information()
