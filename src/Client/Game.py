import pygame
import time
import logging
from src.Client.Client import reconnecting_client
from src.Client.EntitySprite import EntitySpriteManager
from os import getcwd

class Game:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))

        EntitySpriteManager.load_entity_config('/src/utility/animations/'
                                               'melee_animations.json')
        EntitySpriteManager.load_entity_config('/src/utility/animations/'
                                               'player_animations.json')
        from src.Client.MainWindow import MainWindow
        self.active_window = MainWindow((1000, 1000))
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self, ip):
        with reconnecting_client(ip) as client:
            self.active_window.set_client(client)
            while self.running:
                self.clock.tick(100)
                self.screen.fill((0, 0, 0))
                while not client.action_queue.empty():
                    current_action = client.action_queue.get()
                    self.active_window.accept_action(current_action)
                if not client.game_started:
                    time.sleep(0.5)
                    continue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    else:
                        self.active_window.accept_event(event)

                self.active_window.draw(self.screen)
                pygame.display.update()
                pygame.event.pump()


game = Game()
