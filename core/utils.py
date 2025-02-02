from __future__ import annotations

import os
import pickle
import pygame

from dataclasses import dataclass
from typing import Optional, Union, Sequence, Tuple

from core.const import SCREEN_HEIGHT, SCREEN_WIDTH, BLOCK_SIZE


@dataclass
class TextStyle:
    text_colour: Union[int, str, Sequence[int]]
    text_bg_colour: Optional[Union[int, str, Sequence[int]]] = None
    bold: bool = False
    italic: bool = False
    font_name: Optional[Union[str, bytes]] = None

    def copy(self) -> TextStyle:
        return TextStyle(
            text_colour=self.text_colour,
            text_bg_colour=self.text_bg_colour,
            bold=self.bold,
            italic=self.italic,
            font_name=self.font_name,
        )


@dataclass
class ButtonStyle:
    button_width: int
    button_height: int
    text_style: TextStyle
    fill_colour: Union[int, str, Sequence[int]] = "black"
    outline_colour: Union[int, str, Sequence[int]] = "green"

    def copy(self) -> ButtonStyle:
        return ButtonStyle(
            button_width=self.button_width,
            button_height=self.button_height,
            text_style=self.text_style,
            fill_colour=self.fill_colour,
            outline_colour=self.outline_colour,
        )


@dataclass
class MusicVol:
    bg_vol: float = 0.5
    sfx_vol: float = 0.5

    def copy(self) -> MusicVol:
        return MusicVol(bg_vol=self.bg_vol, sfx_vol=self.sfx_vol)


class Box:
    __slots__ = ("window", "fill_colour", "outline_colour", "box_rect")

    def __init__(
        self,
        window: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        fill_colour: Union[int, str, Sequence[int]] = "black",
        outline_colour: Union[int, str, Sequence[int]] = "green",
    ) -> None:
        self.window = window
        self.fill_colour = fill_colour
        self.outline_colour = outline_colour
        self.box_rect = pygame.rect.Rect(x, y, width, height)

    def render(self) -> None:
        pygame.draw.rect(self.window, self.fill_colour, self.box_rect, 0, 5)
        pygame.draw.rect(self.window, self.outline_colour, self.box_rect, 2, 5)


class Text:
    __slots__ = ("window", "center", "text_style", "text_size", "font", "rect")

    def __init__(
        self,
        window: pygame.Surface,
        text_style: TextStyle,
        text_size: int,
        center: Tuple[int, int],
    ) -> None:
        self.window = window
        self.center = center
        self.text_style = text_style
        self.font = pygame.font.SysFont(
            self.text_style.font_name,
            text_size,
            self.text_style.bold,
            self.text_style.italic,
        )
        self.rect: Optional[pygame.Rect] = None

    def render(
        self,
        text: str,
        colour: Optional[Union[int, str, Sequence[int]]] = None,
        text_bg_colour: Optional[Union[int, str, Sequence[int]]] = None,
        antialias: bool = True,
    ) -> None:
        rendered_text = self.font.render(
            text,
            antialias,
            colour or self.text_style.text_colour,
            text_bg_colour or self.text_style.text_bg_colour,
        )
        if self.rect is None:
            self.rect = rendered_text.get_rect(center=self.center)
        self.window.blit(rendered_text, self.rect)


class Button:
    __slots__ = (
        "window",
        "text",
        "button_style",
        "__clicked",
        "button_text",
        "button_rect",
    )

    def __init__(
        self,
        window: pygame.Surface,
        text: str,
        x: int,
        y: int,
        text_size: int,
        button_style: ButtonStyle,
    ) -> None:
        self.window = window
        self.text = text
        self.button_style = button_style
        self.__clicked = False

        self.button_text = Text(
            self.window,
            self.button_style.text_style,
            text_size,
            (x, y + self.button_style.button_height // 2),
        )
        self.button_rect = pygame.rect.Rect(
            x - self.button_style.button_width // 2,
            y,
            self.button_style.button_width,
            self.button_style.button_height,
        )

    def render(self) -> None:
        """Manually render the buttons."""

        pygame.draw.rect(
            self.window, self.button_style.fill_colour, self.button_rect, 0, 5
        )
        pygame.draw.rect(
            self.window,
            self.button_style.outline_colour,
            self.button_rect,
            2,
            5,
        )
        self.button_text.render(self.text)

    def click(self) -> bool:
        """Should manually be called when pygame.MOUSEBUTTONDOWN event has been dispatched."""

        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos):
            return True
        return False

    def run(self) -> bool:
        """Handles rendering & click events automatically (buggy)."""

        self.render()
        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.__clicked:
                self.__clicked = True
                return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.__clicked = False

        return False


class Slider:
    button_down: bool = False
    target: Optional[Slider] = None
    __slots__ = (
        "window",
        "width",
        "initial",
        "value",
        "additional",
        "clamp",
        "min_pos",
        "max_pos",
        "slider_img",
        "slider_rect",
        "slider_path",
    )

    def __init__(
        self,
        window: pygame.Surface,
        slider_img: pygame.Surface,
        x: int,
        y: int,
        initial: float = 0.0,
    ) -> None:
        self.width = 100  # The length of the slider path
        self.window = window

        self.min_pos = x
        self.max_pos = x + self.width

        self.additional = self.min_pos / 100
        self.value = initial
        preset_x = (initial + self.additional) * self.width

        self.clamp = False
        self.slider_img = slider_img
        self.slider_rect = slider_img.get_rect(center=(preset_x, y))
        self.slider_path = pygame.Rect(x, y, self.width, 1)

    def run(self) -> None:
        pygame.draw.rect(self.window, "white", self.slider_path)
        self.window.blit(self.slider_img, self.slider_rect)

        if self.button_down:
            pos = pygame.mouse.get_pos()
            if (Slider.target is None or Slider.target == self) and (
                self.slider_rect.collidepoint(pos) or self.clamp
            ):
                self.clamp = True
                Slider.target = self
                self.slider_rect.centerx = max(
                    min(self.max_pos, pos[0]), self.min_pos
                )
                self.value = round(
                    (self.slider_rect.centerx / self.width) - self.additional,
                    2,
                )
        else:
            self.clamp = False
            Slider.target = None


def draw_grid(window: pygame.Surface) -> None:
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            line = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(window, (255, 255, 255), line, 1)


def load_highscore(path: str) -> int:
    if not os.path.isfile(path=path):
        save_highscore(path=path, score=1)
        return 1

    with open(path, "rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return 1


def save_highscore(path: str, score: int) -> None:
    with open(path, "wb") as f:
        pickle.dump(score, f)


def load_settings(path: str) -> MusicVol:
    if not os.path.isfile(path=path):
        save_settings(path=path, settings=MusicVol())
        return MusicVol()

    with open(path, "rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return MusicVol()


def save_settings(path: str, settings: MusicVol) -> None:
    with open(path, "wb") as f:
        pickle.dump(settings, f)
