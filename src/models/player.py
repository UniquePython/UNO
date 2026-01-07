from dataclasses import dataclass
from typing import List

from models.cards import Card
from models.colors import Color


@dataclass
class Player:
    hand: List[Card]
    
    @staticmethod
    def choose_color() -> Color:
        while True:
            choice = input("Choose a color (RED, YELLOW, GREEN, BLUE): ").upper()
            try:
                return Color[choice]
            except KeyError:
                print("Invalid color. Try again.")
    
    @staticmethod
    def choose_card(playable_cards: list[Card]) -> Card:
        print("Playable cards:")
        for i, card in enumerate(playable_cards):
            print(f"{i}: {card}")

        while True:
            try:
                choice = int(input("Choose a card to play: "))
                return playable_cards[choice]
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")

    def __str__(self) -> str:
        return "Cards = " + ", ".join(str(card) for card in self.hand)
