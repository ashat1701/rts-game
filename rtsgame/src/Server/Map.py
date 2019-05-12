import random

from rtsgame.src.utility.constants import *
from rtsgame.src.utility.utilities import level_to_tile


class Map:
    def room_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]
        for current_room in room_list:
            if (x < (current_room[0] + current_room[2]) and
                    current_room[0] < (x + w) and
                    y < (current_room[1] + current_room[3]) and
                    current_room[1] < (y + h)):
                return True
        return False

    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0
        w = random.randint(self.min_room_len, self.max_room_len)
        h = random.randint(self.min_room_len, self.max_room_len)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))
        return [x, y, w, h]

    def join_rooms(self, room_1, room_2):
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])
        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1
        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1
        if x1 < (x2 + w2) and x2 < (
                x1 + w1):  # Если комнаты накладываются по x
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)
        elif y1 < (y2 + h2) and y2 < (y1 + h1):  # Аналогично по y
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)
        else:  # Буква Г
            join = random.randint(0,
                                  1)  # Выбираем сторону в которую повернута буква Г
            if join == 0:  # Неправильная буква Г - вправо-вверх
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2,
                                                             jy2, 0)
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2,
                                                             jy2, 1)
                    self.corridor_list.append(corridors)
            else:  # Правильная буква Г - вверх вправо
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2,
                                                             jy2, 1)
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2,
                                                             jy2, 0)
                    self.corridor_list.append(corridors)

    def __init__(self, width, height, max_rooms, min_room_len, max_room_len,
                 random_connections):
        self.height = height
        self.min_room_len = min_room_len
        self.random_connections = random_connections
        self.max_room_len = max_room_len
        self.width = width
        self.max_rooms = max_rooms
        self.level = []
        for i in range(self.height):
            self.level.append([STONE] * self.width)
        self.room_list = []
        self.corridor_list = []

        for a in range(self.max_rooms * 5):
            tmp_room = self.gen_room()
            if not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room_list = self.room_list[:]
                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)
            if len(self.room_list) >= self.max_rooms:
                break

        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        for room_num, room in enumerate(self.room_list):  # Комнаты
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = FLOOR

        for corridor in self.corridor_list:  # Корридоры|
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = FLOOR
            if len(corridor) == 3:
                x3, y3 = corridor[2]
                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = FLOOR

        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == FLOOR:
                    if self.level[row - 1][col - 1] == STONE:
                        self.level[row - 1][col - 1] = WALL
                    if self.level[row - 1][col] == STONE:
                        self.level[row - 1][col] = WALL

                    if self.level[row - 1][col + 1] == STONE:
                        self.level[row - 1][col + 1] = WALL

                    if self.level[row][col - 1] == STONE:
                        self.level[row][col - 1] = WALL

                    if self.level[row][col + 1] == STONE:
                        self.level[row][col + 1] = WALL

                    if self.level[row + 1][col - 1] == STONE:
                        self.level[row + 1][col - 1] = WALL

                    if self.level[row + 1][col] == STONE:
                        self.level[row + 1][col] = WALL

                    if self.level[row + 1][col + 1] == STONE:
                        self.level[row + 1][col + 1] = WALL
        self._tile = level_to_tile(self.level)

    #  tile_type{0 - free space; 1 - wall}
    def set(self, x, y, tile_type):
        self._tile[x][y] = tile_type

    def get(self, x, y):
        # Саша пров-=ерь
        x = int(x)
        y = int(y)
        return self._tile[x][y]

    def corridor_between_points(self, x1, y1, x2, y2, param=2):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:  # Прямой
            return [(x1, y1), (x2, y2)]
        else:
            if param == 1:
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif param == 0:
                return [(x1, y1), (x2, y1), (x2, y2)]


if __name__ == "__main__":
    map = Map(height=60, width=60, max_rooms=7, max_room_len=8, min_room_len=8,
              random_connections=3)
    for i in map._tile:
        for j in i:
            if (j == -1):
                print("#", end="")
            else:
                print(j, end="")
        print()
