import pygame
import time
from src.Client.Client import reconnecting_client
from src.Client.EntitySprite import EntitySpriteManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))

        EntitySpriteManager.load_entity_config('/src/utility/animations/'
                                               'melee_animations.json')
        self._tile = None  # Гриша
        from src.Client.MainWindow import MainWindow
        self.active_window = MainWindow((500, 500))
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        with reconnecting_client('127.0.0.1') as client:
            self.active_window.set_client(client)
            while self.running:
                self.clock.tick(40)
                self.screen.fill((0, 0, 0))
                while not client.action_queue.empty():
                    current_action = client.action_queue.get()
                    self.active_window.accept_action(current_action)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    else:
                        self.active_window.accept_event(event)

                self.active_window.draw(self.screen)
                pygame.display.update()
                pygame.event.pump()


game = Game()
