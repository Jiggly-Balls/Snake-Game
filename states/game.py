import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from game_state import State
from game_state.errors import ExitGameError

from core.const import (
    BASE_FPS,
    BG_MUSIC_PATH,
    BLOCK_SIZE,
    DEATH_SFX_PATH,
    EAT_SFX_PATH,
    HIGHSCORE_PATH,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_UP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SNAKE_COLOUR,
)
from core.entities import Apple, Snake
from core.utils import (
    draw_grid,
    load_highscore,
    save_highscore,
    Button,
    MusicVol,
    Text,
)
from core.preset import blue_text_style, red_text_style, red_button_style


class Game(State):
    def __init__(self, volume: MusicVol) -> None:
        self.volume = volume

        self.bg_music = pygame.mixer.Sound(BG_MUSIC_PATH)
        self.death_sound = pygame.mixer.Sound(DEATH_SFX_PATH)
        self.eat_sound = pygame.mixer.Sound(EAT_SFX_PATH)

        death_style = red_text_style.copy()
        death_style.bold = True
        self.death_text = Text(
            self.window, death_style, 30, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.score_text = Text(
            self.window,
            blue_text_style,
            100,
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10),
        )
        self.highscore_text = Text(
            self.window,
            blue_text_style,
            50,
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1),
        )

        self.restart_button = Button(
            self.window,
            "Restart",
            SCREEN_WIDTH / 2.4,
            SCREEN_HEIGHT / 1.8,
            25,
            red_button_style,
        )
        self.menu_button = Button(
            self.window,
            "Menu",
            SCREEN_WIDTH / 1.7,
            SCREEN_HEIGHT / 1.8,
            25,
            red_button_style,
        )

    def run(self) -> None:
        snake = Snake()
        apple = Apple.spawn(snake=snake)
        self.bg_music.set_volume(self.volume.bg_vol)
        self.death_sound.set_volume(self.volume.sfx_vol)
        self.eat_sound.set_volume(self.volume.sfx_vol)
        self.bg_music.play(-1)

        death_play = False
        move = False  # For handling rapid key strokes; allows only a single keystroke every frame.
        fps = BASE_FPS
        highscore = load_highscore(HIGHSCORE_PATH)

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

                if event.type == KEYDOWN:
                    if not move:
                        if snake.x_dir != 1 and (event.key in KEY_LEFT):
                            snake.x_dir = snake.x_dir or -1
                            snake.y_dir = 0
                            move = True
                        elif snake.x_dir != -1 and (event.key in KEY_RIGHT):
                            snake.x_dir = snake.x_dir or 1
                            snake.y_dir = 0
                            move = True
                        elif snake.y_dir != -1 and (event.key in KEY_UP):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or -1
                            move = True
                        elif snake.y_dir != 1 and (event.key in KEY_DOWN):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or 1
                            move = True

                if (
                    snake.dead
                    and event.type == MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    if self.restart_button.click():
                        self.manager.update_state()
                        # If you use this method before manager.change_state, it will reset the current state.

                    elif self.menu_button.click():
                        self.manager.change_state("Menu")
                        self.manager.update_state()

            if snake.head.x == apple.x and snake.head.y == apple.y:
                self.eat_sound.play()
                last_body = snake.body[-1]
                snake.body.append(
                    pygame.Rect(
                        last_body.x, last_body.y, BLOCK_SIZE, BLOCK_SIZE
                    )
                )
                apple = Apple.spawn(snake=snake)
                if len(snake.body) % 4 == 0:
                    fps += 1

            apple.update(self.window)
            snake.update()
            draw_grid(self.window)

            pygame.draw.rect(self.window, SNAKE_COLOUR, snake.head, BLOCK_SIZE)
            move = False
            for body in snake.body:
                pygame.draw.rect(self.window, SNAKE_COLOUR, body, BLOCK_SIZE)

            self.score_text.render(f"{len(snake.body)}")
            self.highscore_text.render(f"HIGHSCORE: {highscore}")

            if snake.dead:
                self.bg_music.stop()
                if not death_play:
                    self.death_sound.play()
                    death_play = True

                self.death_text.render("You have died!")
                self.restart_button.render()
                self.menu_button.render()
                # self.restart_text.render("Click anywhere on the screen to restart.")

                if len(snake.body) > highscore:
                    highscore = len(snake.body)
                    save_highscore(HIGHSCORE_PATH, highscore)
                    self.highscore_text.render(f"HIGHSCORE: {highscore}")

            pygame.display.update()
            self.clock.tick(fps)
