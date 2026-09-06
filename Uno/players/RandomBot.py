import random
from Uno.game.Card import *
from Uno.players.Bot import Bot


class BotRandom(Bot):
    def __init__(self, name: str = ""):
        """Initializes bot"""
        super().__init__(name)

    def __str__(self):
        return f":robot:[cyan] Random Bot {self.name}[/]"

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        return random.choice(possible_colors)

    def change_color(self, card: ColorCard):
        card.change_color(self.choose_color())

    def move(self, first_card_taken=None, game=None):
        """Handles a different situations of game state and reacts accordingly"""
        if isinstance(first_card_taken, ColorCard):
            self.change_color(first_card_taken)

        if first_card_taken is not None:
            return first_card_taken

        valid_cards = self.valid_cards(first_card_taken)
        card_to_play = random.choice(valid_cards)
        if isinstance(card_to_play, ColorCard):
            self.change_color(card_to_play)
        return card_to_play
