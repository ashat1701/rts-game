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
        from src.Client.SIOServer import sio, run
        time.sleep(1)
        run()
        self.active_window.set_sio(sio)

        while self.running:
            self.clock.tick(100)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    if self.active_window.running_game:
                        self.active_window.accept_event(event)

            self.active_window.draw(self.screen)
            pygame.display.update()
            pygame.event.pump()

    def accept_action(self, action):
        self.active_window.accept_action(action)


game = Game()
