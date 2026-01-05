from typing import List, Tuple
import random

from models.cards import *
from models.colors import Color
from models.numbers import Number
from models.actions import Action, WildAction
from models.player import Player


def create_deck() -> List[Card]:
    deck: List[Card] = []
    
    for color in Color:
        for number in Number:
            if number == 0:
                deck.append(NumberCard(color, number))
            else:
                for _ in range(2):
                    deck.append(NumberCard(color, number))
        
        for action in Action:
            for _ in range(2):
                deck.append(ActionCard(color, action))
        
    for wild_action in WildAction:
        for _ in range(4):
                deck.append(WildCard(wild_action))
    
    return deck


def distribute_cards(deck: List[Card], num_players: int) -> Tuple[List[Card], List[Player]]:
    if not 2 <= num_players <= 10:
        raise ValueError("Number of players must be between 2 and 10 inclusive.")

    if not deck or not all(isinstance(card, Card) for card in deck):
        raise ValueError("Deck does not contain valid cards.")

    if len(deck) < num_players * 7:
        raise ValueError("Not enough cards to distribute.")

    random.shuffle(deck)

    players: List[Player] = []

    for _ in range(num_players):
        hand = [deck.pop() for _ in range(7)]
        players.append(Player(hand))

    return deck, players
