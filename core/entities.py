from __future__ import annotations

import pygame
from random import randint
from typing import List

from core.const import BLOCK_SIZE, APPLE_COLOUR, SCREEN_HEIGHT, SCREEN_WIDTH


class Snake:
    def __init__(self) -> None:
        self.x = BLOCK_SIZE
        self.y = BLOCK_SIZE
        self.x_dir = 1
        self.y_dir = 0
        self.head: pygame.Rect = pygame.Rect(
            self.x, self.y, BLOCK_SIZE, BLOCK_SIZE
        )
        self.body: List[pygame.Rect] = [
            pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
        ]
        self.dead = False

    def update(self) -> None:
        if self.dead:
            self.x_dir = 0
            self.y_dir = 0
        else:
            self.body.append(self.head)
            for i in range(len(self.body) - 1):
                self.body[i].x = self.body[i + 1].x
                self.body[i].y = self.body[i + 1].y

            self.head.x += self.x_dir * BLOCK_SIZE
            self.head.y += self.y_dir * BLOCK_SIZE
            self.body.remove(self.head)

            if self.head.x not in range(
                0, SCREEN_WIDTH
            ) or self.head.y not in range(0, SCREEN_HEIGHT):
                self.dead = True

            if not self.dead:
                for body in self.body:
                    if self.head.x == body.x and self.head.y == body.y:
                        self.dead = True
                        break


class Apple:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, APPLE_COLOUR, self.rect)

    @classmethod
    def spawn(cls, snake: Snake) -> Apple:
        invalid = True
        total_body = [snake.head] + snake.body
        while invalid:
            x = (
                randint(0, SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
            ) * BLOCK_SIZE
            y = (
                randint(0, SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE
            ) * BLOCK_SIZE
            for body in total_body:
                if body.x != x or body.y != y:
                    invalid = False
                else:  # if the condition above isn't met even for a single body; the coordinates are reinitialized.
                    invalid = True
                    break
        return cls(x=x, y=y)
