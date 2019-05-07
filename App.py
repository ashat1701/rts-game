import src.Server.Server as Server
import logging
import queue
from src.Server import Logic
import time
from src.Server.WorldState import World
from src.Server.ActionBuilder import ActionBuilder
from src.Server.Visitor import Visitor


class App:
    def __init__(self, server):
        self.server = server
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()
        self.logic = Logic.Logic()

    def update(self):
        while not self.server.action_queue.empty():
            self.analyze_action(self.server.action_queue.get())
        self.logic.all_npc_start_attack()
        self.logic.move_all_entities()

    def send_information_to_player(self, player_id):
        entities_to_draw = []
        visitor = Visitor()
        for visible_entity_id in self.logic.geometry_system.get_visible_entities(player_id):
            entities_to_draw.append(World.entity[visible_entity_id].accept(visitor))

        self.server.send_obj_to_player(entities_to_draw, player_id)

    def analyze_action(self, action):
        player_id, current_action = action
        if current_action == "PLAYER_CONNECTED":
            self.logic.spawn_system.create_player(player_id)
        if current_action.startswith("MOVE"):
            if current_action == "MOVE_LEFT":
                new_direction = (-1, World.get_direction(player_id)[1])
            if current_action == "MOVE_RIGHT":
                new_direction = (1, World.get_direction(player_id)[1])
            if current_action == "MOVE_UP":
                new_direction = (World.get_direction(player_id)[0], 1)
            if current_action == "MOVE_DOWN":
                new_direction = (World.get_direction(player_id)[0], -1)
            World.set_direction(player_id, new_direction)

        if current_action.startswith("STOP"):
            if current_action == "STOP_MOVE_LEFT":
                new_direction = (0, World.get_direction(player_id)[1])
            if current_action == "STOP_MOVE_RIGHT":
                new_direction = (0, World.get_direction(player_id)[1])
            if current_action == "STOP_MOVE_UP":
                new_direction = (World.get_direction(player_id)[0], 0)
            if current_action == "STOP_MOVE_DOWN":
                new_direction = (World.get_direction(player_id)[0], 0)
            World.set_direction(player_id, new_direction)
            #Костыль
        if current_action != "PLAYER_CONNECTED":
            self.logic.animation_system.continue_or_reset_move_animation(
                player_id,
                World.get_direction(player_id)
            )


if __name__ == '__main__':
    with Server.SafeServer() as server:
        App = App(server)
        logging.basicConfig(level=logging.DEBUG)
        while True:
            time.sleep(0.01)
            App.update()
            App.send_information_to_player(World.get_first_player_id())
            App.send_information_to_player(World.get_second_player_id())
