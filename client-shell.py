import logging

from src.Client.Game import game


logging.basicConfig(level=logging.DEBUG)
game.run("localhost")
