import pygame
from typing import Tuple


BASE_FPS: int = 9
SCREEN_WIDTH: int = 750
SCREEN_HEIGHT: int = 750
BLOCK_SIZE: int = 50  # 25 | 50 | 150 | 250
SNAKE_COLOUR: str = "green"
APPLE_COLOUR: str = "red"
HIGHSCORE_PATH: str = "data.bin"
SETTINGS_PATH: str = "settings.bin"
BG_MUSIC_PATH: str = "assets/bg_music.mp3"
DEATH_SFX_PATH: str = "assets/death_sound.mp3"
EAT_SFX_PATH: str = "assets/eat_sound.mp3"
SLIDER_IMAGE_PATH: str = "assets/slider.png"
KEY_LEFT: Tuple[int, int] = (pygame.K_a, pygame.K_LEFT)
KEY_RIGHT: Tuple[int, int] = (pygame.K_d, pygame.K_RIGHT)
KEY_UP: Tuple[int, int] = (pygame.K_w, pygame.K_UP)
KEY_DOWN: Tuple[int, int] = (pygame.K_s, pygame.K_DOWN)
