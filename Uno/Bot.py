from Card import Card, DrawCard
from Game import *
from Player import *
import time
import random

'''
All        -> 108
Normal     -> 76
Stop       -> 8
Reverse    -> 8
+2         -> 8
All Colors -> 4
+4 Colors  -> 4
'''


class Bot(Player):
    def __init__(self, name):
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

    def update_data(self, *args):
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
        stop_cards = []
        for card in self.hand:
            if isinstance(card, StopCard):
                stop_cards.append(card)
        return stop_cards

    def player_decision(self) -> str:
        if self.turns_to_stop != 0 and len(self.stop_cards) > 0:
            print("Not really")
            return "No"
        elif self.cards_to_take != 0 and (isinstance(self.card_on_top, Plus2Card) and (len(self.plus_2_cards) > 0 or len(self.plus_4_cards) > 0)):
            print("Not really")
            return "No"
        elif self.cards_to_take != 0 and len(self.plus_4_cards) != 0:
            print("Not really")
            return "No"
        else:
            return "Yes"

    def choose_color(self):
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        most_colors = sorted(self.hand, key=lambda card_in_hand: card_in_hand.color)
        for card in most_colors:
            if card.color in possible_colors:
                return card.color
        return random.choice(possible_colors)

    def valid_cards(self):
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top):
                valid_cards_to_put.append(card)
        if len(valid_cards_to_put) > 0:
            return valid_cards_to_put
        else:
            return [DrawCard()]

    def move(self):
        if self.turns_to_stop > 0 and len(self.stop_cards) > 0:
            return random.choice(self.stop_cards)
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            if len(self.plus_2_cards) > 0:
                return random.choice(self.plus_2_cards)
            else:
                return random.choice(self.plus_4_cards)
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            return random.choice(self.plus_4_cards)
        else:
            return random.choice(self.valid_cards())

