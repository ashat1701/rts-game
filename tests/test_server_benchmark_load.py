import os
from src.Server.WorldState import world, recreate_world
from src.Server.Logic import Logic

os.chdir("..")


def spawn_enemies(count, logic):
    for i in range(count):
        logic.spawn_system.create_enemy()
        logic.animation_system.get_animation_state(i + 2)
    assert len(world.entity) == count


def update_animation_and_move(logic):
    logic.move_all_entities()
    for i in range(len(world.entity)):
        logic.animation_system.get_animation_state(i + 2)


def despawn_enemies(count):
    for i in range(count):
        world.delete_entity(i + 2)


def test_animation_system_benchmark(benchmark):
    logic = Logic()
    recreate_world()
    spawn_enemies(60, logic)
    benchmark(update_animation_and_move, logic)
    despawn_enemies(60)
