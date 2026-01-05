from typing import List
from models.cards import *
from models.colors import Color
from models.numbers import Number
from models.actions import Action, WildAction


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

print(len(create_deck()))
for card in create_deck():
    print(card)