from pygame import Rect

from src.Server.Entity import PlayerEntity, MeleeEnemy, RangedEnemy, Projectile
from src.Server.Visitor import Visitor

visitor = Visitor()

player = PlayerEntity().set_box(Rect(0, 0, 20, 20))
melee_enemy = MeleeEnemy().set_box(Rect(100, 100, 10, 10))
range_enemy = RangedEnemy().set_box(Rect(200, 200, 5, 5))
projectile = Projectile().set_box(Rect(300, 300, 10, 10))


def test_player_accept():
    assert player.accept(visitor).get_action() == ((0, 0), 'player', None, None)


def test_melee_enemy_accept():
    assert melee_enemy.accept(visitor).get_action() == ((100, 100), 'melee', None, None)


def test_range_enemy_accept():
    assert range_enemy.accept(visitor).get_action() == ((200, 200), 'range', None, None)


def test_projectile():
    assert projectile.accept(visitor).get_action() == ((300, 300), 'projectile', None, None)
