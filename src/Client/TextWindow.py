import logging

from src.Client.UI.TextWidget import TextContainer
from src.Client.UI.Window import Window
from src.utility.utilities import Vector


class WaitWindow(Window):
    def __init__(self):
        super().__init__()
        text = TextContainer('Waiting! Be comfy, take a cookie.')
        self.add_child(text, Vector(400, 500))
        self.map = None

    def accept_action(self, action):
        if not isinstance(action, list):
            raise RuntimeError(
                "Action is not of type list. Don't know what to do with it")

        if action[0] == "MAP":
            self.map = action[1]
            logging.info("Acquired map")
            self.sio.emit("message", "MAP_RECEIVED")

        if action[0] == "START_GAME":
            from src.Client.Game import game
            game.start_main_window(self.map)
