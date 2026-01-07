from dataclasses import dataclass
from typing import List

from src.models.cards import Card
from src.models.colors import Color


@dataclass
class Player:
    hand: List[Card]
    name: str
    said_uno: bool = False
    human: bool = False
    
    def choose_color(self) -> Color:
        while True:
            choice = input(f"{self.name}, choose a color (RED, YELLOW, GREEN, BLUE): ").upper()
            try:
                return Color[choice]
            except KeyError:
                print("Invalid color. Try again.")
    
    def choose_card(self, playable_cards: list[Card]) -> Card:
        print(f"{self.name}'s playable cards:")
        for i, card in enumerate(playable_cards):
            print(f"{i}: {card}")

        while True:
            try:
                choice = int(input("Choose a card to play: "))
                return playable_cards[choice]
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")

    def __str__(self) -> str:
        return f"{self.name}'s hand: " + ", ".join(str(card) for card in self.hand)