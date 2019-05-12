from src.Client.EntitySprite import EntitySprite
from src.utility.utilities import Vector
from src.utility.constants import PIXEL_SCALE, MAP_SCALE
import os

os.chdir("..")


def test_data_access():
    entity = EntitySprite(((100, 200),
                           'player1',
                           'idle',
                           0,
                           (10, 100)))

    assert entity.position == Vector(100 / MAP_SCALE * PIXEL_SCALE,
                                     200 / MAP_SCALE * PIXEL_SCALE)
    assert entity.type == 'player1'
    assert entity.animation_name == 'idle'
    assert entity.frame == 0
    assert entity.health == 10
