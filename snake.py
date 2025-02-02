__version__ = "2.5"

import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import DOUBLEBUF

from core.const import SETTINGS_PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from core.utils import load_settings
from core.errors import ExitStateError, ExitGameError
from states import StateManager, GAME_STATES


icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)
pygame.mixer.init()
pygame.init()
pygame.display.init()
pygame.display.set_caption("Snake Game v" + __version__)
pygame.event.set_allowed((QUIT, KEYDOWN, MOUSEBUTTONDOWN))


class SnakeGame:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(None)
        self.state_manager = StateManager(
            self.screen, *GAME_STATES, volume=load_settings(SETTINGS_PATH)
        )

    def run(self) -> None:
        self.state_manager.change_state("Menu")
        while True:
            try:
                self.state_manager.run_current_state()
            except ExitStateError:
                pass


if __name__ == "__main__":
    try:
        snake_game = SnakeGame()
        snake_game.run()
    except ExitGameError:
        pygame.quit()
