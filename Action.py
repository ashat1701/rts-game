class PlayerMoveAction:
    def __init__(self, x ,y):
        self.x = x
        self.y = y


class DrawAction:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type