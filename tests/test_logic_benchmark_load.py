import os

from src.Server.Logic import Logic
from src.Server.WorldState import WorldState, world, recreate_world

os.chdir("..")

def spawn_enemies(count, logic):
    for i in range(count):
        logic.spawn_system.create_enemy()
    assert len(world.entity) == count

def despawn_enemies(count):
    for i in range(count):
        world.delete_entity(i + 2)

def test_world_time_creation(benchmark):
    benchmark(recreate_world)

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

def test_move_enteties_stress(benchmark):
    benchmark(move_entities, count=120)

def test_spawn_and_delete_stress(benchmark):
    benchmark(spawn_and_delete_enemies, 120)

def create_map():
    from src.Server.Map import Map
    map = Map(height=200, width=200, random_connections=10, max_rooms=20, min_room_len=10, max_room_len=10)

def test_map_create_time_stress(benchmark):
    benchmark(create_map)
