from src.Server.Entity import PlayerEntity
import os
from src.Server.Logic import Logic
from src.Server.WorldState import WorldState, world
from src.utility.constants import *
os.chdir("..")

def create_enemies(count):
    world = WorldState()
    logic = Logic()
    for i in range(count):
        logic.spawn_system.create_enemy()

def test_enemy_time_creation(benchmark):
    benchmark(create_enemies, count=30)

def test_world_time_creation(benchmark):
    benchmark(WorldState)

def test_spawn_and_dead_time(benchmark):
    benchmark(spawn_and_delete_enemies, 60)

def spawn_and_delete_enemies(count):
    world = WorldState()
    logic = Logic()
    for i in range(count):
        logic.spawn_system.create_enemy()
    for i in range(count):
        world.delete_entity(i)