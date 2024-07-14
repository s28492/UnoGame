from Uno.players.Player import *
from Uno.game.Card import *


class Bot(Player):
    def __init__(self, name: str):
        """Initializes bot"""
        super().__init__(name)
        self.players = None
        self.pile = None
        self.card_on_top = None
        self.direction = None
        self.turns_to_stop = None
        self.cards_to_take = None
        self.stop_cards = []
        self.plus_2_cards = []
        self.plus_4_cards = []
        self.possible_colors = ["Red", "Green", "Blue", "Yellow"]

    def __str__(self):
        return f":robot:[cyan]Bot {self.name}[/]"

    def set_bot_data(self, data) -> None:
        """Updates game data for bot"""
        self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take = data
        self.stop_cards, self.plus_2_cards, self.plus_4_cards = [], [], []
        for card in self.hand:
            if isinstance(card, StopCard):
                self.stop_cards.append(card)
            elif isinstance(card, Plus2Card) and not isinstance(card, Plus4Card):
                self.plus_2_cards.append(card)
            elif isinstance(card, Plus4Card):
                self.plus_4_cards.append(card)


    def stop_card_on_hand(self) -> list:
        """Create and return all stop cards in bot "hand"""
        pass

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        pass

    def valid_cards(self) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        pass

    def change_color(self, card: ColorCard):
        pass

    def move(self, first_card_taken = None):
        """Handles a different situations of game state and reacts accordingly"""
        pass
