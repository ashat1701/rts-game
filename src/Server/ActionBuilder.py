class ActionBuilder:
    def __init__(self):
        self._action = {'box': None, 'type': None, 'animation_name': None, 'frame': None}
        # TODO: изменить box на одну координату (левого верхнего угла)
    def set_box(self, box):
        self._action['box'] = box
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

    def get_animation_state(self):
        return self._action['animation_name'], self._action['frame']

    def get_type(self):
        return self._action['type']
