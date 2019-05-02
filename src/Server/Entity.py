from src.Server.Animation import parse_config
from src.utility.utilities import cls_init
import os

class Entity:
    def __init__(self):
        self._position = None
        self._id = None

    def set_id(self, id):
        self._id = id
        return self

    def set_position(self, position):
        self._position = position
        return self

    def get_position(self):
        return self._position

    def get_id(self):
        return self._id


class MovableEntity(Entity):
    def __init__(self):
        super().__init__()
        self._velocity = None
        self._direction = None

    def set_velocity(self, velocity):
        self._velocity = velocity
        return self

    def set_direction(self, direction):
        self._direction = direction
        return self

    def get_velocity(self):
        return self._velocity

    def get_direction(self):
        return self._direction

    def move(self):
        dx = self._direction[0] * self._velocity
        dy = self._direction[1] * self._velocity
        self._position = (self._position[0] + dx, self._position[1] + dy)


class Enemy(MovableEntity):
    def __init__(self):
        super().__init__()
        self._health = None
        self._damage = None

    def set_health(self, health):
        self._health = health
        return self

    def set_damage(self, damage):
        self._damage = damage
        return self

    def get_health(self):
        return self._health

    def get_damage(self):
        return self._damage

    def attack(self):
        raise NotImplementedError


class Projectile(MovableEntity):
    def __init__(self):
        super().__init__()
        self._damage = None

    def set_damage(self, damage):
        self._damage = damage
        return self

    def get_damage(self):
        return self._damage


# TODO MAKE LOADING ANIMATIONS MORE ROBUST
class MeleeEnemy(Enemy):
    def __init__(self):
        super().__init__()

    dirname = os.path.dirname(__file__)
    animations, directions_binds = parse_config(
        os.path.join(dirname, '../utility/animations/melee_animations.json'))
    default_animation = 'idle'

    def attack(self):
        pass


class RangedEnemy(Enemy):
    def __init__(self):
        super().__init__()

    def attack(self):
        pass
