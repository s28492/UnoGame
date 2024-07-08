from Player import *
import time
import random
from Card import *
from Bot import Bot


class BotRandom(Bot):
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

    def __str__(self):
        return f":robot:[cyan]Bot {self.name}[/]"

    def set_bot_data(self, data) -> None:
        """Updates game data for bot"""
        print("Updating...")
        self.players, self.pile, self.card_on_top, self.direction \
            , self.turns_to_stop, self.cards_to_take = data
        self.stop_cards, self.plus_2_cards, self.plus_4_cards = [], [], []
        for card in self.hand:
            if isinstance(card, StopCard):
                self.stop_cards.append(card)
            elif isinstance(card, Plus2Card) and not isinstance(card, Plus4Card):
                self.plus_2_cards.append(card)
            elif isinstance(card, Plus4Card):
                self.plus_4_cards.append(card)
        print("Updated.\ncard on top: ", self.card_on_top)


    def stop_card_on_hand(self) -> list:
        """Create and return all stop cards in bot "hand"""
        stop_cards = []
        for card in self.hand:
            if isinstance(card, StopCard):
                stop_cards.append(card)
        return stop_cards

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        most_colors = sorted(self.hand, key=lambda card_in_hand: card_in_hand.color)
        for card in most_colors:
            if card.color in possible_colors:
                return card.color
        return random.choice(possible_colors)

    def when_list_arrived(self):
        for card in self.hand:
            if isinstance(card, list):
                return 10/0
    def valid_cards(self) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        self.when_list_arrived()
        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards_plus_2 = self.collect_valid_cards_of_given_instance(Plus2Card)
            valid_cards_plus_4 = self.collect_valid_cards_of_given_instance(Plus4Card)
            if len(valid_cards_plus_2) > 0:
                return valid_cards_plus_2
            elif len(valid_cards_plus_4) > 0:
                return valid_cards_plus_4
            else:
                return [DrawCard()]

        valid_cards = self.collect_valid_cards_of_given_instance(Card)

        return valid_cards if len(valid_cards) > 0 else [DrawCard()]


    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []
        print(self.card_on_top)
        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                valid_cards_to_put.append(card)
        return valid_cards_to_put


    def change_color(self, card: ColorCard):
        card.change_color(random.choice(["Red", "Green", "Blue", "Yellow"]))

    def move(self, first_card_taken = None):
        """Handles a different situations of game state and reacts accordingly"""
        if first_card_taken is not None:
            return first_card_taken
        valid_cards = self.valid_cards()
        card_to_play = random.choice(valid_cards)
        if isinstance(card_to_play, ColorCard):
            self.change_color(card_to_play)
        return card_to_play
