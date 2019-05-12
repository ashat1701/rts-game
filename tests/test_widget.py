from src.Client.UI.Widget import Widget
from src.utility.utilities import Vector

import os
os.chdir("..")


def test_child_draw():
    widget = Widget()
    widget_pos = Vector(100, 300)

    class FakeChild:
        def __init__(self, pos):
            self.pos = Vector(*pos)

        def draw(self, surface, abs_position):
            assert abs_position == self.pos + widget_pos

    child1 = FakeChild((100, 100))
    child2 = FakeChild((100, 200))

    widget.add_child(child1, Vector(*child1.pos))
    widget.add_child(child2, Vector(*child2.pos))

    widget.draw(None, widget_pos)

