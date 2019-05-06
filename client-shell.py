import logging

from src.Client.Game import game

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    game.run()
