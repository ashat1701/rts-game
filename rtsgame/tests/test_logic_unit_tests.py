import os

from src.Server.Entity import PlayerEntity
from src.Server.Logic import Logic
from src.Server.WorldState import world
from src.utility.constants import *

os.chdir("..")

logic = Logic()


def test_player_spawn():
    logic.spawn_system.create_player(0)
    assert isinstance(world.entity[0], PlayerEntity)
    assert len(world.entity) == 1
    assert len(world.enemies) == 0
    assert len(world.movable_entities) == 1


def test_player_spawn_propereties():
    assert world.get_health(0) == PLAYER_HEALTH
    assert world.get_damage(0) == PLAYER_START_DAMAGE
    assert world.get_velocity(0) == PLAYER_VELOCITY


def test_single_enemy_spawn():
    logic.spawn_system.create_enemy()
    assert len(world.entity) == 2
    assert len(world.enemies) == 1


def test_damage_deal():
    logic.damage_system.deal_damage(0, 2)
    enemy_start_health = world.get_health(2)
    player_damage = world.get_damage(0)
    if player_damage >= enemy_start_health:
        assert len(world.dead_entities) == 1
    else:
        assert world.get_health(2) == enemy_start_health - player_damage


def test_player_move():
    initial_position = world.get_box(0).center
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        world.set_direction(0, direction)
        dx, dy = [i * world.get_velocity(0) for i in direction]

        temp_box = world.get_box(0).move(dx, dy)
        if logic.geometry_system.collide_with_wall(temp_box):
            logic.move(0)
            assert initial_position == world.get_box(0).center

        for other_entity_id in world.entity.keys():
            if logic.geometry_system.collide(temp_box, world.get_box(other_entity_id)) and 0 != other_entity_id:
                logic.move(0)
                assert initial_position == world.get_box(0).center
                break
        else:
            logic.move(0)
            new_position = world.get_box(0).center
            assert new_position != initial_position
            initial_position = new_position
