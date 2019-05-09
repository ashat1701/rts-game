import src.Server.Server as Server
import logging
import queue
import os
from src.Server import Logic
import time
from src.Server.WorldState import world
from src.Server.ActionBuilder import ActionBuilder
from src.Server.Visitor import Visitor

player1_connected = False
player2_connected = False


class App:
    def __init__(self, server):
        self.server = server
        self.logic = Logic.Logic()

    def get_all_entity_information(self, entity_id, visitor):
        return world.entity[entity_id].accept(visitor). \
            set_animation_state(*self.logic.animation_system.get_animation_state(entity_id)).get_action()

    def send_world_state_to_player(self, player_id):
        entities_to_draw = []
        visitor = Visitor()
        for visible_entity_id in self.logic.geometry_system.get_visible_entities(player_id):
            entities_to_draw.append(self.get_all_entity_information(visible_entity_id, visitor))
        self.server.send_obj_to_player(entities_to_draw, player_id)

    def send_map_to_player(self, player_id):
        self.server.send_obj_to_player(world.map._tile, player_id)

    def update(self):
        while not self.server.action_queue.empty():
            self.analyze_action(self.server.action_queue.get())
        self.logic.move_all_entities()
        self.logic.update_attack_state()

        self.send_world_state_to_player(world.get_first_player_id())  # Add second player
        if len(world.enemies) < 20:
            self.logic.spawn_system.create_enemy()
        # self.send_world_state_to_player(world.get_second_player_id())

    def analyze_action(self, action):
        player_id, current_action = action
        if current_action == "PLAYER_CONNECTED":
            self.logic.spawn_system.create_player(player_id)

        if current_action.startswith("MOVE"):
            if current_action == "MOVE_LEFT":
                new_direction = (-1, world.get_direction(player_id)[1])
            if current_action == "MOVE_RIGHT":
                new_direction = (1, world.get_direction(player_id)[1])
            if current_action == "MOVE_UP":
                new_direction = (world.get_direction(player_id)[0], -1)
            if current_action == "MOVE_DOWN":
                new_direction = (world.get_direction(player_id)[0], 1)

            if current_action == "MOVE_LEFT_STOP":
                new_direction = (0, world.get_direction(player_id)[1])
            if current_action == "MOVE_RIGHT_STOP":
                new_direction = (0, world.get_direction(player_id)[1])
            if current_action == "MOVE_UP_STOP":
                new_direction = (world.get_direction(player_id)[0], 0)
            if current_action == "MOVE_DOWN_STOP":
                new_direction = (world.get_direction(player_id)[0], 0)
            world.set_direction(player_id, new_direction)
            if world.get_last_attack(world.get_first_player_id()) is None:
                self.logic.animation_system.continue_or_reset_move_animation(
                    player_id,
                    world.get_direction(player_id)
                )

        if current_action == 'ATTACK':
            self.logic.start_attack(world.get_first_player_id(),
                                    world.get_direction(world.get_first_player_id()))


class GameLoop:
    def __init__(self, app):
        self.app = app

    def run(self):
        while True:
            time.sleep(0.01)
            self.app.update()


def start_game(game_mode="Singleplayer"):
    with Server.SafeServer() as server:
        server.start_as_daemon()
        if game_mode == "Singleplayer":
            connected_players = [player1_connected]
        if game_mode == "Multiplayer":
            connected_players = [player1_connected, player2_connected]
        while not all(connected_players):
            time.sleep(0.5)
            current_action = server.action_queue.get()
            if current_action[1] == "PLAYER_CONNECTED":
                connected_players[current_action[0]] = True

        new_app = App(server)
        for id in range(len(connected_players)):
            new_app.logic.spawn_system.create_player(id)
            new_app.logic.animation_system.get_animation_state(id)  # Create in animation set
        server.send_obj_all_players(["MAP", world.map.level])
        logging.info("Sent map to everyone")

        game_loop = GameLoop(new_app)

        game_loop.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.path.dirname(os.path.abspath(__file__))
    start_game()
