import os

from rtsgame.src.Server.Logic import Logic
from rtsgame.src.Server.WorldState import world

os.chdir("..")
logic = Logic()


def test_delete():
    logic.spawn_system.create_enemy()
    assert len(world.enemies) == 1
    assert len(world.entity) == 1
    assert len(world.movable_entities) == 1
    world.delete_entity(2)
    assert len(world.enemies) == 0
    assert len(world.entity) == 0
    assert len(world.movable_entities) == 0
