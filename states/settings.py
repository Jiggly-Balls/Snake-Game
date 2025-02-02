import pygame

from pygame import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from game_state import State
from game_state.errors import ExitGameError

from core.utils import (
    MusicVol,
    Box,
    Text,
    Button,
    Slider,
    draw_grid,
    save_settings,
)
from core.const import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SLIDER_IMAGE_PATH,
    SETTINGS_PATH,
)
from core.preset import blue_text_style, blue_button_style


class Settings(State):
    def __init__(self, volume: MusicVol) -> None:
        self.volume = volume

        self.fps = 30

        self.slider_img = pygame.image.load(SLIDER_IMAGE_PATH).convert()
        # self.slider_img = pygame.transform.scale(self.slider_img, (20, 20))

        box_width = SCREEN_WIDTH // 1.5
        box_height = SCREEN_HEIGHT // 1.2
        self.box = Box(
            self.window,
            (SCREEN_WIDTH - box_width) // 2,
            (SCREEN_HEIGHT - box_height) // 2,
            box_width,
            box_height,
        )

        settings_style = blue_text_style.copy()
        settings_style.bold = True
        self.settings_text = Text(
            self.window,
            settings_style,
            60,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT / 4),
        )
        self.bg_vol_text = Text(
            self.window,
            blue_text_style,
            25,
            (SCREEN_WIDTH // 3, SCREEN_HEIGHT / 2.2),
        )
        self.sfx_vol_text = Text(
            self.window,
            blue_text_style,
            25,
            (SCREEN_WIDTH // 3, SCREEN_HEIGHT / 1.8),
        )

        self.back_button = Button(
            self.window,
            "Back",
            SCREEN_WIDTH // 3.1,
            SCREEN_HEIGHT // 1.21,
            30,
            blue_button_style,
        )

    def run(self) -> None:
        music_slider = Slider(
            self.window,
            self.slider_img,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2.2,
            self.volume.bg_vol,
        )
        sfx_slider = Slider(
            self.window,
            self.slider_img,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.8,
            self.volume.sfx_vol,
        )
        music_val_text = Text(
            self.window,
            blue_text_style,
            25,
            (SCREEN_WIDTH // 1.4, SCREEN_HEIGHT // 2.2),
        )
        sfx_val_text = Text(
            self.window,
            blue_text_style,
            25,
            (SCREEN_WIDTH // 1.4, SCREEN_HEIGHT // 1.8),
        )

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
                    Slider.button_down = True

                    if self.back_button.click():
                        self.volume.bg_vol = music_slider.value
                        self.volume.sfx_vol = sfx_slider.value

                        save_settings(SETTINGS_PATH, self.volume)

                        self.manager.change_state("Menu")
                        self.manager.update_state()

                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    Slider.button_down = False

            draw_grid(self.window)
            self.box.render()

            self.settings_text.render("Settings")
            self.bg_vol_text.render("Music Volume")
            self.sfx_vol_text.render("SFX Volume")

            music_slider.run()
            sfx_slider.run()

            music_val_text.render(f"{round(music_slider.value * 100)}%")
            sfx_val_text.render(f"{round(sfx_slider.value * 100)}%")

            self.back_button.render()

            pygame.display.update()
            self.clock.tick(self.fps)
