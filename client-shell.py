import pygame
from src.Client.Client import reconnecting_client
import logging
import time
from queue import Queue
from src.Client.EntitySprite import MeleeSprite


# class Frontend:
#     def __init__(self):
#         os.environ['SDL_VIDEO_CENTERED'] = '1'
#         pygame.init()
#         pygame.display.set_caption(SCREEN_TITLE)
#         pygame.mouse.set_visible(False)
#         self.fullscreen = False
#         self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
#                                               pygame.HWSURFACE | pygame.DOUBLEBUF)


logging.basicConfig(level=logging.DEBUG)
pygame.init()

screen = pygame.display.set_mode((500, 500))

running = True
x = 250
y = 250
x1 = 250
y1 = 250


entities = {}
# player = Melee(0, 0, 'idle', frame=0)
# right_pressed = False
# clock = pygame.time.Clock()
# duration = 200
# time_left = duration
# while running:
#     screen.fill((255, 255, 255))
#     tick_time = clock.tick(30)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 logging.info("Pressed R")
#                 right_pressed = True
#
#         elif event.type == pygame.KEYUP:
#             if event.key == pygame.K_RIGHT:
#                 logging.info("Released R")
#                 time_left = duration
#                 right_pressed = False
#
#     if right_pressed:
#         if player.cur_animation != 'run':
#             time_left = duration
#             player.set_sprite('run', 0)
#         else:
#             time_left -= tick_time
#             if time_left < 0:
#                 time_left = duration
#                 player.set_sprite('run', player.frame + 1)
#             player.x = player.x + tick_time / 1000 * 10
#     else:
#         if player.cur_animation != 'idle':
#             time_left = duration
#             player.set_sprite('idle', 0)
#         else:
#             time_left -= tick_time
#             if time_left < 0:
#                 time_left = duration
#                 player.set_sprite('idle', player.frame + 1)
#
#     screen.blit(player.get_sprite(), (player.x, player.y))
#     pygame.display.update()
player = MeleeSprite(0, 0, 'idle', frame=0)
clock = pygame.time.Clock()
with reconnecting_client(addr='127.0.0.1') as client:
    while running:
        clock.tick(20)
        screen.fill((0, 0, 0))
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        while not client.action_queue.empty():
            current_action = client.action_queue.get()[0]
            player.set_position(current_action[0], current_action[1])
            player.set_animation(current_action[3], current_action[4])
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
            client.send_object("STOP")
        screen.blit(player.get_sprite(), (player.x, player.y))
        pygame.display.update()
        pygame.event.pump()
    pygame.quit()
