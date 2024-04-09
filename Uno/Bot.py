from Game import *
from Player import *
import time
import random

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

    def __str__(self):
        return f":robot:[cyan]Bot {self.name}[/]"

    def update_data(self, *args) -> None:
        """Updates game data for bot"""
        while True:
            self.players, self.pile, self.card_on_top, self.direction \
                , self.turns_to_stop, self.cards_to_take = args[0].get_bot_data()
            self.stop_cards, self.plus_2_cards, self.plus_4_cards = [], [], []
            for card in self.hand:
                if isinstance(card, StopCard):
                    self.stop_cards.append(card)
                elif isinstance(card, Plus2Card) and not isinstance(card, Plus4Card):
                    self.plus_2_cards.append(card)
                elif isinstance(card, Plus4Card):
                    self.plus_4_cards.append(card)
            time.sleep(0.03)

    def stop_card_on_hand(self) -> list:
        """Create and return all stop cards in bot "hand"""
        stop_cards = []
        for card in self.hand:
            if isinstance(card, StopCard):
                stop_cards.append(card)
        return stop_cards

    def player_decision(self) -> str:
        """If bot can deny taking or being stopped it will, if not he accepts his fate"""
        if self.turns_to_stop != 0 and len(self.stop_cards) > 0:
            print("Not really")
            return "No"
        elif self.cards_to_take != 0 and (
                isinstance(self.card_on_top, Plus2Card) and (len(self.plus_2_cards) > 0 or len(self.plus_4_cards) > 0)):
            print("Not really")
            return "No"
        elif self.cards_to_take != 0 and len(self.plus_4_cards) != 0:
            print("Not really")
            return "No"
        else:
            return "Yes"

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        most_colors = sorted(self.hand, key=lambda card_in_hand: card_in_hand.color)
        for card in most_colors:
            if card.color in possible_colors:
                return card.color
        return random.choice(possible_colors)

    def valid_cards(self) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top):
                valid_cards_to_put.append(card)
        if len(valid_cards_to_put) > 0:
            return valid_cards_to_put
        else:
            return [DrawCard()]

    def move(self) -> Card:
        """Handles a different situations of game state and reacts accordingly"""
        # If bot could be stopped it plays stop card
        if self.turns_to_stop > 0 and len(self.stop_cards) > 0:
            return random.choice(self.stop_cards)
        # If Plus2Card was played it reacts with Plus2Cards or Plus4Cards card
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            if len(self.plus_2_cards) > 0:
                return random.choice(self.plus_2_cards)
            else:
                return random.choice(self.plus_4_cards)
        # if Plus4Cards was played it reacts with Plus4Card card
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            return random.choice(self.plus_4_cards)
        # If there are no unusual states it picks random card from those possible to play
        else:
            return random.choice(self.valid_cards())
