from pygame import Rect

from rtsgame.src.Server.Entity import PlayerEntity, MeleeEnemy, RangedEnemy, Projectile
from rtsgame.src.Server.Visitor import Visitor
from rtsgame.src.Server.WorldState import world

visitor = Visitor()

player = PlayerEntity().set_box(Rect(0, 0, 20, 20)).set_id(0).set_health(50)

melee_enemy = MeleeEnemy().set_box(Rect(100, 100, 10, 10))
range_enemy = RangedEnemy().set_box(Rect(200, 200, 5, 5))
projectile = Projectile().set_box(Rect(300, 300, 10, 10))
world.entity[0] = player


def test_player_accept():
    assert player.accept(visitor).get_action() == ((0, 0), 'player1', None, None, (50, 100))


def test_melee_enemy_accept():
    assert melee_enemy.accept(visitor).get_action() == ((100, 100), 'melee', None, None, None)


def test_range_enemy_accept():
    assert range_enemy.accept(visitor).get_action() == ((200, 200), 'range', None, None, None)


def test_projectile():
    assert projectile.accept(visitor).get_action() == ((300, 300), 'projectile', None, None, None)
