from constants import *
import queue
import Server
import logging
import time
import random
import Action

# 0 - first player
# 1 - second player


class Map:
    def __init__(self):
        self._tile = [[0] * MAX_X for _ in range(MAX_Y)]
        for i in range(MAX_Y):
            self.set(0, i, WALL)
            self.set(MAX_X - 1, i, WALL)
        for i in range(MAX_X):
            self.set(i, 0, WALL)
            self.set(i, MAX_Y - 1, WALL)

    #  tile_type{0 - free space; 1 - wall}
    def set(self, x, y, tile_type):
        self._tile[x][y] = tile_type

    def get(self, x, y):
        return self._tile[x][y]


class World:
    def __init__(self):
        self.server = Server.SafeServer()
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()

        # Components
        self._position = {}
        self._health = {}
        self._damage = {}
        self._velocity = {}
        self._enemy = set()

        self.map = Map()

        self._current_id = -1
        self.first_player = self.create_entity(position=(1, 1), health=100, damage=50)
        self.second_player = self.create_entity(position=(MAX_X - 2, MAX_Y - 2))
        self.test_enemy = self.create_entity(position=(MAX_X // 2, MAX_Y // 2), health=100)
        self.add_enemy(self.test_enemy)

    def create_entity(self, position=None, health=None, damage=None) -> int:
        self._current_id += 1
        if position is not None:
            self._position[self._current_id] = position
        if health is not None:
            self._health[self._current_id] = health
        if damage is not None:
            self._damage[self._current_id] = damage
        return self._current_id

    def add_enemy(self, entity_id):
        self._enemy.add(entity_id)

    def get_position(self, entity_id):
        return self._position[entity_id]

    def move(self, entity_id, dx, dy):
        x = self._position[entity_id][0]
        y = self._position[entity_id][1]
        if self.map.get(x + dx, y + dy) == 0:
            self.map.set(x + dx, y + dy, 2)
            self.map.set(x, y, 0)
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
            if current_action == "UP":
                self.move(player_id, 0, -1)
                self.server.send_obj_to_player(Action.PlayerMoveAction(*self.get_position(self.first_player)),
                                               self.first_player)
            if current_action == "DOWN":
                self.move(player_id, 0, 1)
                self.server.send_obj_to_player(Action.PlayerMoveAction(*self.get_position(self.first_player)),
                                               self.first_player)
            if current_action == "LEFT":
                self.move(player_id, -1, 0)
                self.server.send_obj_to_player(Action.PlayerMoveAction(*self.get_position(self.first_player)),
                                               self.first_player)
            if current_action == "RIGHT":
                self.move(player_id, 1, 0)
                self.server.send_obj_to_player(Action.PlayerMoveAction(*self.get_position(self.first_player)),
                                               self.first_player)
            if current_action == "ATTACK":
                self.attack(player_id)

        self.move_all_npc()

    def send_information(self):
        visible_entities = self.get_visible_entities(self.first_player)
        for visible_entity in visible_entities:
            if visible_entity in self._enemy:
                self.server.send_obj_to_player(Action.DrawAction(*self.get_position(visible_entity), "ENEMY"), self.first_player)


if __name__ == '__main__':
    world = World()
    while True:
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        world.update()
        world.send_information()
