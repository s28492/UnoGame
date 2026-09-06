from Uno.players.Player import *
from Uno.game.Card import *
from abc import ABC, abstractmethod


class Bot(Player, ABC):
    def __init__(self, name: str= ""):
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
        self.all_color_cards = []

    def __str__(self):
        return f"{self.name}"

    def set_bot_turns_to_stop(self, turns_to_stop):
        self.turns_to_stop = turns_to_stop

    def set_bot_cards_to_take(self, cards_to_take):
        self.cards_to_take = cards_to_take


    def rich_str(self):
        return f":robot:[bold cyan]{self.name}[/]"

    def get_name(self):
        return self.name

    def set_bot_data(self, data) -> None:
        """Updates game data for bot"""
        self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take = data
        self.stop_cards, self.plus_2_cards, self.plus_4_cards, self.all_color_cards = [], [], [], []
        
        for card in self.hand:
            if isinstance(card, StopCard):
                self.stop_cards.append(card)
            elif isinstance(card, Plus2Card) and not isinstance(card, Plus4Card):
                self.plus_2_cards.append(card)
            elif isinstance(card, Plus4Card):
                self.plus_4_cards.append(card)
            elif isinstance(card, ColorCard):
                self.all_color_cards.append(card)

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        return max(self.count_colors_in_hand(), key=self.count_colors_in_hand().get)

    def get_hand(self):
        return self.hand

    def set_hand(self, cards):
        self.hand = cards

    def change_color(self, card: ColorCard):
        pass

    @abstractmethod
    def move(self, first_card_taken = None, game=None):
        """Handles a different situations of game state and reacts accordingly"""
        pass
