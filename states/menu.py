import pygame

from pygame import QUIT, MOUSEBUTTONDOWN
from game_state import State
from game_state.errors import ExitGameError

from core.utils import MusicVol, Box, Text, Button, draw_grid
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT
from core.preset import blue_button_style, blue_text_style


class Menu(State):
    def __init__(self, volume: MusicVol) -> None:
        self.volume = volume

        self.fps = 60
        self.play_button = Button(
            self.window,
            "Play",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) - 75,
            25,
            blue_button_style,
        )
        self.settings_button = Button(
            self.window,
            "Settings",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            25,
            blue_button_style,
        )
        self.quit_button = Button(
            self.window,
            "Quit",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) + 75,
            25,
            blue_button_style,
        )

        title_style = blue_text_style.copy()
        title_style.bold = True
        self.title_text = Text(
            self.window,
            title_style,
            100,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5),
        )

        box_width = SCREEN_WIDTH // 2.2
        box_height = SCREEN_HEIGHT // 2
        self.box = Box(
            self.window,
            (SCREEN_WIDTH - box_width) // 2,
            (SCREEN_HEIGHT - box_height) // 1.7,
            box_width,
            box_height,
        )

    def run(self) -> None:
        while True:
            self.window.fill(
                (
                    0,
                    0,
                    0,
                )
            )

            for event in pygame.event.get():
                if event.type == QUIT:
                    raise ExitGameError()

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_button.click():
                        self.manager.change_state("Game")
                        self.manager.update_state()

                    elif self.settings_button.click():
                        self.manager.change_state("Settings")
                        self.manager.update_state()

                    elif self.quit_button.click():
                        raise ExitGameError()

            draw_grid(self.window)
            self.box.render()
            self.play_button.render()
            self.settings_button.render()
            self.quit_button.render()
            self.title_text.render("SNAKE GAME")

            pygame.display.update()
            self.clock.tick(self.fps)
