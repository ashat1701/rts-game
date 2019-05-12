import logging

import pygame

from src.Client.EntitySprite import EntitySpriteManager


class Game:
    def __init__(self):
        logging.basicConfig(filename='game.log', filemode='w',
                            level=logging.INFO)
        self.screen = None
        self.clock = None
        self.active_window = None
        self.running = True

    def start_main_window(self, level_map):
        from src.Client.MainWindow import MainWindow
        main_window = MainWindow((1000, 1000), self.active_window.sio)
        main_window.main_camera.set_map(level_map)
        self.active_window = main_window

    def run(self, ip):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))

        EntitySpriteManager.load_entity_config('src/utility/animations/'
                                               'melee_animations.json')
        EntitySpriteManager.load_entity_config('src/utility/animations/'
                                               'player1_animations.json')
        EntitySpriteManager.load_entity_config('src/utility/animations/'
                                               'player2_animations.json')
        self.clock = pygame.time.Clock()

        from src.Client.TextWindow import WaitWindow
        self.active_window = WaitWindow()

        from src.Client.SIOServer import sio, run
        self.active_window.set_sio(sio)
        run(ip)

        while self.running:
            self.clock.tick(30)
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    # Key logger
                    if event.type == pygame.KEYDOWN:
                        logging.info("Pressed key {}".format(event.unicode))

                    self.active_window.accept_event(event)

            self.active_window.draw(self.screen)
            pygame.display.update()
            pygame.event.pump()

        sio.disconnect()

    def accept_action(self, action):
        self.active_window.accept_action(action)


game = Game()
