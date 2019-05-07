from src.Server.AnimationSystem import parse_config
from src.utility.utilities import cls_init
import os
from ..utility.constants import *


class Entity:
    def __init__(self):
        self._id = None
        self.box = None # box - это хитбокс (pygame.rect для готовой геометрии)

    def accept(self, visitor):
        raise NotImplementedError

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

    def set_box(self, box):
        self.box = box
        return self

    def get_box(self):
        return self.box


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
        self.box.move_ip(dx, dy)


class Enemy(MovableEntity):
    def __init__(self):
        super().__init__()
        self._health = None
        self._damage = None
        self._attack_reload = None
        self._last_attack = None

    def set_health(self, health):
        self._health = health
        return self

    def set_last_attack(self, last_attack):
        self._last_attack = last_attack
        return self

    def get_last_attack(self):
        return self._last_attack

    def set_attack_reload(self, attack_reload):
        self._attack_reload = attack_reload
        return self

    def set_damage(self, damage):
        self._damage = damage
        return self

    def get_attack_reload(self):
        return self._attack_reload

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
        self._health = 0

    def accept(self, visitor):
        visitor.visit_projectile(self)

    def set_damage(self, damage):
        self._damage = damage
        return self

    def get_damage(self):
        return self._damage

    def get_health(self):
        return self._health


# TODO MAKE LOADING ANIMATIONS MORE ROBUST
class MeleeEnemy(Enemy):
    def __init__(self):
        super().__init__()


    def accept(self, visitor):
        visitor.visit_melee_enemy(self)

    dirname = os.path.dirname(__file__)
    animations, direction_binds = parse_config(
        os.path.join(dirname, '../utility/animations/melee_animations.json'))
    default_animation = 'idle'

    def attack(self):
        pass


class RangedEnemy(Enemy):
    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        visitor.visit_ranged_enemy(self)

    dirname = os.path.dirname(__file__)
    animations, direction_binds = parse_config(
        os.path.join(dirname, '../utility/animations/melee_animations.json'))
    default_animation = 'idle'

    def attack(self):
        pass

class PlayerEntity(MovableEntity):
    def __init__(self):
        super().__init__()
        self._damage = PLAYER_START_DAMAGE
        self._health = PLAYER_HEALTH
        self._attack_reload = None
        self._last_attack = None

    def accept(self, visitor):
        visitor.visit_player(self) # Надо ещё передать инфу о том, какой это Player. (может их айди будут в константах?)

    def set_last_attack(self, last_attack):
        self._last_attack = last_attack
        return self

    def get_last_attack(self):
        return self._last_attack

    def set_attack_reload(self, attack_reload):
        self._attack_reload = attack_reload
        return self

    dirname = os.path.dirname(__file__)
    animations, direction_binds = parse_config(
        os.path.join(dirname, '../utility/animations/melee_animations.json'))
    default_animation = 'idle'

    def set_damage(self, damage):
        self._damage = damage
        return self

    def get_damage(self):
        return self._damage

    def get_health(self):
        return self._health

    def set_health(self, health):
        self._health = health
        return self