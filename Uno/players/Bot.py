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


    def count_colors_in_hand(self):
        return {color: sum(1 for card in self.hand if card.color == color) for color in self.possible_colors}


    def create_card_instance(self, card_value: str, card_color: str = None):
        if card_value == "+4":
            card = Plus4Card(card_value, card_color)
            if card_color == "Colors" or card_color == "Color":
                card.change_color(self.choose_color())
            else:
                card.change_color(card_color)

        elif card_value == "All":
            card = ColorCard(card_value, card_color)
            if card_color == "Colors" or card_color == "Color":
                card.change_color(self.choose_color())
            else:
                card.change_color(card_color)
        elif card_value == "Stop" and card_color is None:
            card = StopCard(card_value, card_value)
        elif card_value == "Stop" and card_color is not None:
            card = StopCard(card_value, card_color)
        elif card_value == "+2":
            card = Plus2Card(card_value, card_color)
        elif card_value == "Reverse":
            card = ReverseCard(card_value, card_color)
        elif card_value == "Draw":
            card = DrawCard()
        else:
            card = Card(card_value, card_color)
        return card

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
