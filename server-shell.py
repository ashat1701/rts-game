from constants import *
import queue
import Server
import logging
import time

# 0 - first player
# 1 - second player


class World:
    def __init__(self):
        self.server = Server.SafeServer()
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()
        self._current_id = 1
        self.first_player_id = 0
        self.second_player_id = 1
        self._position = {}
        self.add_position(self.first_player_id, 0, 0)
        self._velocity = {}
        self._enemy = set()
        self._tile = [[0] * MAX_X for _ in range(MAX_Y)]

    #  tile_type{0 - free space; 1 - wall}
    def set(self, x, y, tile_type):
        self._tile[x][y] = tile_type

    def get(self, x, y):
        return self._tile[x][y]

    #  TODO: algorithm of creating walls
    def create_map(self):
        for i in range(MAX_Y):
            self.set(0, i, 1)
            self.set(MAX_X - 1, i, 1)
        for i in range(MAX_X):
            self.set(i, 0, 1)
            self.set(i, MAX_Y - 1, 1)

    def create_entity(self) -> int:
        self._current_id += 1
        return self._current_id

    def add_position(self, entity_id, x, y):
        self._position[entity_id] = (x, y)

    def add_enemy(self, entity_id):
        self._enemy.add(entity_id)

    def get_position(self, entity_id):
        return self._position[entity_id]

    def move(self, entity_id, dx, dy):
        x = self._position[entity_id][0]
        y = self._position[entity_id][1]
        if self._tile[x + dx][y + dy] == 0:
            self._position[entity_id] = (x + dx, y + dy)

    # TODO: analyze walls
    @staticmethod
    def _is_visible(position1: tuple, position2: tuple) -> bool:
        return (position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2 < VISION_RANGE

    def get_nearby_entities(self, entity_id) -> list:
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
                self.move(player_id, 0, 5)

    def send_information(self):
        self.server.send_obj_to_player(self.get_position(self.first_player_id), self.first_player_id)


if __name__ == '__main__':
    world = World()
    while True:
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        world.update()
        world.send_information()
