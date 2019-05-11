import logging

from src.Client.Game import game

# import eventlet
# eventlet.monkey_patch()

logging.basicConfig(level=logging.DEBUG)
game.run("localhost")
