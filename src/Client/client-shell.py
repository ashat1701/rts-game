import pygame
import logging
from .Client import Client
from ..Server import ActionBuilder
import time

pygame.init()

screen = pygame.display.set_mode((500, 500))

running = True
x = 250
y = 250
with Client.reconnecting_client(addr='127.0.0.1') as client:
    while running:
        screen.fill((0, 0, 0))
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        while not client.action_queue.empty():
            current_action = client.action_queue.get()
            if type(current_action) == ActionBuilder.PlayerMoveAction:
                x = current_action.x
                y = current_action.y
            if type(current_action) == ActionBuilder.DrawAction:
                if current_action.type == "ENEMY":
                    pygame.draw.rect(screen, (255, 0, 0), (current_action.x, current_action.y, 50, 50))

            print(current_action)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            client.send_object("MOVE_LEFT")
        if keys[pygame.K_RIGHT]:
            client.send_object("MOVE_RIGHT")
        if keys[pygame.K_UP]:
            client.send_object("MOVE_UP")
        if keys[pygame.K_DOWN]:
            client.send_object("MOVE_DOWN")
        if keys[pygame.K_SPACE]:
            client.send_object("ATTACK")
        pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 50))
        pygame.display.update()
        pygame.event.pump()
    pygame.quit()
