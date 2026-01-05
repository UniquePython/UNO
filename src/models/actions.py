from enum import Enum, auto


class Action(Enum):
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    WILD = auto()
    WILD_DRAW_FOUR = auto()