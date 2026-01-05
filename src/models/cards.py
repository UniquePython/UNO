from dataclasses import dataclass
from enum import Enum, auto

from models.colors import Color
from models.numbers import Number 
from models.actions import Action


class Card:
    pass


@dataclass
class NumberCard(Card):
    color: Color
    number: Number


@dataclass
class ActionCard(Card):
    color: Color
    action: Action


class WildCard(Card, Enum):
    WILD = auto()
    WILD_DRAW_FOUR = auto()