from dataclasses import dataclass

from src.models.colors import Color
from src.models.numbers import Number 
from src.models.actions import Action, WildAction


class Card:
    pass


@dataclass
class NumberCard(Card):
    color: Color
    number: Number
    
    def __str__(self):
        return f"{self.color.name} {self.number.name}"


@dataclass
class ActionCard(Card):
    color: Color
    action: Action
    
    def __str__(self):
        return f"{self.color.name} {self.action.name}"


@dataclass
class WildCard(Card):
    action: WildAction
    
    def __str__(self):
        return f"{self.action.name}"