from __future__ import annotations

from states.game import Game
from states.menu import Menu
from states.settings import Settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple
    from game_state import State

__all__ = ("Game", "Menu", "Settings")
GAME_STATES: Tuple[State, ...] = (Game, Menu, Settings)
