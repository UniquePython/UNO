import random
from dataclasses import dataclass
from typing import List, Literal

from src.models.numbers import Number
from src.models.cards import Card, NumberCard, ActionCard, WildCard
from src.models.colors import Color
from src.models.actions import Action, WildAction
from src.models.player import Player
from src.models.ai import SmartAI, SimpleAI, RandomAI


# -------------------- Helpers --------------------

def next_player(index: int, direction: int, n: int) -> int:
    return (index + direction) % n


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


def distribute_cards(deck: List[Card], players: List[Player]) -> List[Card]:

    if not deck or not all(isinstance(card, Card) for card in deck):
        raise ValueError("Deck does not contain valid cards.")

    if len(deck) < len(players) * 7:
        raise ValueError("Not enough cards to distribute.")

    random.shuffle(deck)

    for player in players:
        player.hand = [deck.pop() for _ in range(7)]

    return deck

# -------------------- Game State --------------------

@dataclass
class GameState:
    draw_pile: List[Card]
    discard_pile: List[Card]
    current_player: int
    direction: Literal[-1, 1]
    current_color: Color
    pending_draw: int = 0
    skip_next: bool = False


# -------------------- Core Rules --------------------

def is_playable(card: Card, top: Card, color: Color, hand: List[Card]) -> bool:
    if isinstance(card, WildCard):
        if card.action == WildAction.WILD_DRAW_FOUR:
            return not any(
                isinstance(c, (NumberCard, ActionCard)) and c.color == color
                for c in hand
            )
        return True

    if isinstance(card, NumberCard):
        return card.color == color or (
            isinstance(top, NumberCard) and card.number == top.number
        )

    if isinstance(card, ActionCard):
        return card.color == color or (
            isinstance(top, ActionCard) and card.action == top.action
        )

    return False


def apply_action(card: Card, state: GameState, players: List[Player]):
    if isinstance(card, ActionCard):
        if card.action == Action.SKIP:
            state.skip_next = True

        elif card.action == Action.REVERSE:
            if len(players) == 2:
                state.skip_next = True
            else:
                state.direction *= -1 # pyright: ignore[reportAttributeAccessIssue]

        elif card.action == Action.DRAW_TWO:
            state.pending_draw += 2
            state.skip_next = True

    elif isinstance(card, WildCard):
        state.current_color = players[state.current_player].choose_color()

        if card.action == WildAction.WILD_DRAW_FOUR:
            state.pending_draw += 4
            state.skip_next = True


def play_card(card: Card, state: GameState, players: List[Player]):
    player = players[state.current_player]

    if card not in player.hand:
        raise ValueError("Card not in hand")

    if not is_playable(card, state.discard_pile[-1], state.current_color, player.hand):
        raise ValueError("Illegal move")

    player.hand.remove(card)
    state.discard_pile.append(card)

    if isinstance(card, (NumberCard, ActionCard)):
        state.current_color = card.color

    apply_action(card, state, players)


# -------------------- Turn Resolution --------------------

def end_turn(state: GameState, players: List[Player]):
    n = len(players)
    target = next_player(state.current_player, state.direction, n)

    if state.pending_draw:
        for _ in range(state.pending_draw):
            if not state.draw_pile:
                reshuffle(state)
            players[target].hand.append(state.draw_pile.pop())
        state.pending_draw = 0

    if state.skip_next:
        state.skip_next = False
        state.current_player = next_player(target, state.direction, n)
    else:
        state.current_player = target


def draw_card(player: Player, state: GameState) -> Card:
    if not state.draw_pile:
        reshuffle(state)

    card = state.draw_pile.pop()
    player.hand.append(card)
    return card


def reshuffle(state: GameState):
    top = state.discard_pile.pop()
    state.draw_pile = state.discard_pile[:]
    random.shuffle(state.draw_pile)
    state.discard_pile = [top]


def take_turn(player: Player, state: GameState, players: List[Player]):
    top = state.discard_pile[-1]

    playable = [
        c for c in player.hand
        if is_playable(c, top, state.current_color, player.hand)
    ]

    if playable:
        card = player.choose_card(playable)
        play_card(card, state, players)
        print(f"{player.name} plays {card}")
    else:
        drawn = draw_card(player, state)
        if is_playable(drawn, top, state.current_color, player.hand):
            play_card(drawn, state, players)

    end_turn(state, players)


# -------------------- Game Start --------------------

def start_game(deck: List[Card], players: List[Player]) -> GameState:
    random.shuffle(deck)

    while True:
        first = deck.pop()
        if not isinstance(first, WildCard) or first.action != WildAction.WILD_DRAW_FOUR:
            break
        deck.insert(0, first)

    discard = [first]

    if isinstance(first, WildCard):
        color = players[0].choose_color()
    else:
        color = first.color # pyright: ignore[reportAttributeAccessIssue]

    state = GameState(
        draw_pile=deck,
        discard_pile=discard,
        current_player=0,
        direction=1,
        current_color=color,
    )

    if isinstance(first, (ActionCard, WildCard)):
        apply_action(first, state, players)
        end_turn(state, players)

    return state


# -------------------- Main Loop --------------------

def run_game(deck: List[Card], players: List[Player]):
    state = start_game(deck, players)

    while True:
        player = players[state.current_player]
        if getattr(player, 'human', True):
            hand_str = ", ".join(str(card) for card in player.hand)
            print(f"Your cards are: {hand_str}")
        take_turn(player, state, players)

        if len(player.hand) == 1 and not getattr(player, 'said_uno', False):
            print(f"{player.name} says UNO!")
            player.said_uno = True

        if len(player.hand) == 0:
            print(f"{player.name} wins!")
            break


def main():
    n = int(input("Enter total number of players: "))
    
    if not 2 <= n <= 10:
        raise ValueError("Number of players must be between 2 and 10 inclusive.")

    # Create player list
    players = []

    human_name = input("Enter your name: ")
    players.append(Player(hand=[], name=human_name, human=True))  # human player

    names = ["Rudy", "Sharlene", "Rosalie", "Thomas", "Jimmie", "Gail", "Terri", "Christina", "Isabel", "Garfield", "Jonathon", "Jordan", "Horace"]
    
    # Fill remaining with AI
    for _ in range(1, n):
        ai_type = random.choice([RandomAI, SimpleAI, SmartAI])
        players.append(ai_type(hand=[], name=f"{random.choice(names)}"))

    # Prepare deck and deal cards
    deck = create_deck()
    deck = distribute_cards(deck, players)

    run_game(deck, players)


if __name__ == "__main__":
    main()