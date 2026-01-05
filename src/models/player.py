from dataclasses import dataclass
from typing import List

from models.cards import Card


@dataclass
class Player:
    cards: List[Card]
    
    def __str__(self) -> str:
        return "Cards = " + ", ".join(str(card) for card in self.cards)
