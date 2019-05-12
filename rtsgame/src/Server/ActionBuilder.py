class ActionBuilder:
    def __init__(self):
        self._action = {'position': None, 'type': None, 'animation_name': None, 'frame': None,
                        'hp': None}

    def set_position(self, left_top_corner):
        self._action['position'] = left_top_corner
        return self

    def set_type(self, type_):
        self._action['type'] = type_
        return self

    def set_animation_state(self, name, frame):
        self._action['animation_name'] = name
        self._action['frame'] = frame
        return self

    def get_action(self):
        return tuple(self._action.values())

    def set_hp(self, curr_hp, max_hp):
        self._action['hp'] = (curr_hp, max_hp)
        return self
