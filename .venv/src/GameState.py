from enum import Enum, auto


class GameState(Enum):
    MAIN_MENU = auto()
    LEVEL_SELECT = auto()
    GAMEPLAY = auto()
