class Entity:
    def __init__(self, position, id):
        self._position = position
        self._id = id


class MoveableEntity(Entity):
    def __init__(self, position, id, velocity, direction):
        super().__init__(position, id)
        self._velocity = velocity
        self._direction = direction

    def move(self, direction):
        self._direction = direction
        dx = self._direction[0] * self._velocity
        dy = self._direction[1] * self._velocity
        self._position = (self._position[0] + dx, self._position[1] + dy)


class Enemy(MoveableEntity):
    def __init__(self, position, id, velocity, direction, health, damage):
        super().__init__(position, id, velocity, direction)
        self._health = health
        self._damage = damage

    def attack(self):
        raise NotImplementedError


class Projectile(MoveableEntity):
    def __init__(self, position, id, velocity, direction):
        super().__init__(position, id, velocity, direction)


class MeleeEnemy(Enemy):
    pass