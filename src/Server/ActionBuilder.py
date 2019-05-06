class ActionBuilder:
    def __init__(self, action_dict=None):
        if action_dict is None:
            self._action = {'box': None, 1: None, 2: None, 3: None, 4: None}
        else:
            self._action = action_dict

    def set_box(self, box):
        self._action['box'] = box
        return self
    def set_type(self, type_):
        self._action[2] = type_
        return self

    def set_animation_state(self, name, frame):
        self._action[3] = name
        self._action[4] = frame
        return self

    def get_action(self):


    def get_animation_state(self):
        return self._action[3], self._action[4]

    def get_x(self):
        return self._action[0]

    def get_y(self):
        return self._action[1]

    def get_type(self):
        return self._action[2]
