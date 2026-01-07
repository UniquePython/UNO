import random
from collections import Counter
from src.models.player import Player
from src.models.colors import Color
from src.models.cards import NumberCard, ActionCard, WildCard

class RandomAI(Player):
    
    def choose_card(self, playable_cards):
        return random.choice(playable_cards)
    
    def choose_color(self):
        return random.choice(list(Color))


class SimpleAI(Player):
    
    def choose_card(self, playable_cards):
        non_wild = [c for c in playable_cards if not isinstance(c, WildCard)]
        if non_wild:
            action_cards = [c for c in non_wild if isinstance(c, ActionCard)]
            return action_cards[0] if action_cards else non_wild[0]
        return playable_cards[0]

    def choose_color(self):
        colors = [
            c.color for c in self.hand
            if isinstance(c, (NumberCard, ActionCard))
        ]
        if not colors:
            return random.choice(list(Color))
        return Counter(colors).most_common(1)[0][0]

class SmartAI(Player):
    
    def choose_card(self, playable_cards):
        # 1. Prefer action cards
        action = [c for c in playable_cards if isinstance(c, ActionCard)]
        if action:
            return action[0]

        # 2. Avoid wilds unless necessary
        non_wild = [c for c in playable_cards if not isinstance(c, WildCard)]
        if non_wild:
            return non_wild[0]

        # 3. Otherwise play wild
        return playable_cards[0]

    def choose_color(self):
        counts = Counter(
            c.color for c in self.hand
            if isinstance(c, (NumberCard, ActionCard))
        )
        if not counts:
            return random.choice(list(Color))
        return counts.most_common(1)[0][0]
