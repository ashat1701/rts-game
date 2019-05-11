from src.Server.WorldState import world
from src.Server.Logic import Logic
import os
os.chdir("..")
logic = Logic()


def test_delete():
    logic.spawn_system.create_enemy()
    assert len(world.enemies) == 1
    assert len(world.entity) == 1
    assert len(world.movable_entities) == 1
    world.delete_entity(1)
    assert len(world.enemies) == 0
    assert len(world.entity) == 0
    assert len(world.movable_entities) == 0