"""
This file contains classes related to screen management / screen changing.
"""

from __future__ import annotations

import pygame
from typing import Dict, Optional, Generator

from core.errors import StateError, ExitStateError


class State:
    def __init__(self, /, window: pygame.Surface, manager: StateManager) -> None:
        self.window = window
        self.manager = manager
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        """The method to be executed by the StateManager when called."""


class StateManager:
    __slots__ = ("__states", "__current_state")

    def __init__(self, window: pygame.Surface, *states: State, **kwargs) -> None:
        for state in states:
            assert issubclass(
                state, State
            ), f"Expected subclass of `{State}` instead got `{state.__mro__[-2]}`."

        self.__states: Dict[str, State] = {
            class_.__name__: class_(window, self, **kwargs) for class_ in states
        }
        self.__current_state: Optional[State] = None

    def change_state(self, state_name: str) -> None:
        assert (
            state_name in self.__states
        ), f"State `{state_name}` isn't present from the available states: `{', '.join(self.get_all_states())}`."
        self.__current_state = self.__states[state_name]

    def get_state(self) -> Optional[State]:
        return self.__current_state

    def get_all_states(self) -> Generator[str]:
        return (state for state in self.__states.keys())

    def run_current_state(self) -> None:
        if self.__current_state is not None:
            self.__current_state.run()
        else:
            raise StateError("No state has been set to run.")

    def exit_current_state(self) -> None:
        if self.__current_state is not None:
            raise ExitStateError()
        else:
            raise StateError("No state has been set to exit from.")
