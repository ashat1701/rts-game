from constants import *


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