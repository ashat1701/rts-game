import os
from rtsgame.src.Server.Logic import Logic
from rtsgame.src.Server.WorldState import WorldState, world

os.chdir("..")

def spawn_enemies(count, logic):
    for i in range(count):
        logic.spawn_system.create_enemy()
    assert len(world.entity) == count

def despawn_enemies(count):
    for i in range(count):
        world.delete_entity(i + 2)

def test_world_time_creation(benchmark):
    benchmark(WorldState)

def test_spawn_and_dead_time(benchmark):
    benchmark(spawn_and_delete_enemies, 60)

def spawn_and_delete_enemies(count):
    logic = Logic()
    spawn_enemies(count, logic)
    despawn_enemies(count)

def move_entities(count):
    logic = Logic()
    spawn_enemies(count, logic)
    logic.move_all_entities()
    despawn_enemies(count)

def test_move_entities(benchmark):
    benchmark(move_entities, count=60)

