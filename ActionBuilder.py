class ActionBuilder:
    def __init__(self, action_dict=None):
        if action_dict is None:
            self._action = {}
        else:
            self._action = action_dict

    def set_x(self, x):
        self._action[0] = x
        return self

    def set_y(self, y):
        self._action[1] = y
        return self

    def set_type(self, type_):
        self._action[2] = type_
        return self

    def set_animation(self, name):
        self._action[3] = name
        return self

    def set_frame(self, frame):
        self._action[4] = frame
        return self

    def get_action(self):
        return self._action

    def get_animation(self):
        return self._action[3]

    def get_frame(self):
        return self._action[4]

    def get_x(self):
        return self._action[0]

    def get_y(self):
        return self._action[1]

    def get_type(self):
        return self._action[2]
