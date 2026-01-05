from dataclasses import dataclass

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


@dataclass
class WildCard(Card):
    action: Action