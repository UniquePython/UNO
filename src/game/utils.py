import random
from dataclasses import dataclass
from typing import List, Literal

from models.cards import Card, NumberCard, ActionCard, WildCard
from models.colors import Color
from models.actions import Action, WildAction
from models.player import Player


# -------------------- Helpers --------------------

def next_player(index: int, direction: int, n: int) -> int:
    return (index + direction) % n


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
        take_turn(player, state, players)

        if len(player.hand) == 1:
            print(f"{player} says UNO!")

        if len(player.hand) == 0:
            print(f"{player} wins!")
            break
