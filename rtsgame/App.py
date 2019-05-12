import eventlet

eventlet.monkey_patch()
import logging
import os

from rtsgame.src.Server import Logic
from rtsgame.src.Server.Server import Server
from rtsgame.src.Server.Visitor import Visitor
from rtsgame.src.Server.WorldState import world
import rtsgame.src.Server.Server

player1_connected = False
player2_connected = False


class App:
    def __init__(self, server):
        self.server = server

        self.logic = Logic.Logic()

    def get_all_entity_information(self, entity_id, visitor):
        return world.entity[entity_id].accept(visitor). \
            set_animation_state(
            *self.logic.animation_system.get_animation_state(
                entity_id)).get_action()

    def send_world_state_to_player(self, player_id):
        entities_to_draw = []
        visitor = Visitor()
        spectate_id = player_id
        if world.player_dead[player_id]:
            spectate_id = (player_id + 1) % 2
        entities_to_draw.append(self.get_all_entity_information(spectate_id, visitor))
        for visible_entity_id in self.logic.geometry_system.get_visible_entities(spectate_id):
            if visible_entity_id != spectate_id:
                entities_to_draw.append(
                    self.get_all_entity_information(visible_entity_id, visitor))
        self.server.send_obj_to_player(entities_to_draw, player_id)

    def update(self):

        if rtsgame.src.Server.Server.player_disconnected:
            exit()
        for dead_id in world.dead_entities:
            if dead_id in (world.get_first_player_id(), world.get_second_player_id()):
                self.server.send_obj_to_player(["SPECTATE"], dead_id)
                world.player_dead[dead_id] = True
                if all(world.player_dead):
                    exit()
            self.logic.animation_system.remove_entity(dead_id)
            world.delete_entity(dead_id)
        world.dead_entities = []

        while not self.server.action_queue.empty():
            self.analyze_action(self.server.action_queue.get())
        self.logic.update_enemies_direcion()
        self.logic.move_all_entities()
        self.logic.update_attack_state()

        self.send_world_state_to_player(world.get_first_player_id())
        if world.get_game_mode() == "Multiplayer":
            self.send_world_state_to_player(world.get_second_player_id())

        if len(world.enemies) < 15:
            self.logic.spawn_system.create_enemy()

    def analyze_action(self, action):
        player_id, current_action = action
        if world.player_dead[player_id]:
            return
        if current_action == "PLAYER_CONNECTED":
            self.logic.spawn_system.create_player(player_id)

        if current_action == 'ATTACK':
            self.logic.start_attack(player_id, world.get_direction(player_id))

        if current_action[0] == 'MOVE':
            world.set_direction(player_id, tuple(current_action[1]))
            if world.get_last_attack(player_id) is None:
                self.logic.animation_system.continue_or_reset_move_animation(
                    player_id,
                    world.get_direction(player_id)
                )

    def run(self):
        while True:
            eventlet.sleep(0.1)
            self.update()


def start_game(game_mode="Singleplayer"):
    server = Server()
    server.start()

    if game_mode == "Singleplayer":
        connected_players = [player1_connected]
        world.set_game_mode("Singleplayer")
    if game_mode == "Multiplayer":
        connected_players = [player1_connected, player2_connected]
        world.set_game_mode("Multiplayer")
    while not all(connected_players):
        eventlet.sleep(0.5)
        current_action = server.action_queue.get()
        if current_action[1] == "PLAYER_CONNECTED":
            connected_players[current_action[0]] = True

    app = App(server)
    for id in range(len(connected_players)):
        app.logic.spawn_system.create_player(id)
        app.logic.animation_system.get_animation_state(
            id)  # Create in animation set
    server.send_obj_all_players(["MAP", world.map.level])
    logging.info("Sent map to everyone. waiting")
    while server.action_queue.qsize() < len(connected_players):
        eventlet.sleep(1)

    logging.info("MAP_RECEIVED_ON_SERVER")
    for i in range(len(connected_players)):
        server.action_queue.get()
    for i in range(15):
        app.logic.spawn_system.create_enemy()
    server.send_obj_all_players(["START_GAME"])
    app.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.path.dirname(os.path.abspath(__file__))
    start_game()
