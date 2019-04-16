class ActionBuilder:
    _action = {}

    def get_action(self):
        return self._action

    def set_x(self, x):
        self._action[0] = x

    def set_y(self, y):
        self._action[1] = y

    def set_type(self, type):
        self._action[2] = type

    def get_x(self):
        return self._action[0]

    def get_y(self):
        return self._action[1]

    def get_type(self):
        return self._action[2]
