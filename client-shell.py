import pygame
import Client
from queue import Queue

pygame.init()

screen = pygame.display.set_mode((500, 500))

running = True
x = 250
y = 250
with Client.reconnecting_client(addr='127.0.0.1') as client:
    while running:
        while not client.action_queue.empty():
            current_action = client.action_queue.get()
            x = current_action[0]
            y = current_action[1]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            client.send_object("LEFT")
        if keys[pygame.K_RIGHT]:
            client.send_object("RIGHT")
        if keys[pygame.K_UP]:
            client.send_object("UP")
        if keys[pygame.K_DOWN]:
            client.send_object("DOWN")

        pygame.event.pump()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 50))
        pygame.display.update()
    pygame.quit()
