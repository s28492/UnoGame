import pandas as pd
import random
import os
import pickle
import sys
from Uno.game.Card import ColorCard, Plus4Card, StopCard, DrawCard, Plus2Card, Card, ReverseCard
from Uno.players.Bot import Bot


class BaseAIBot (Bot):
    def __init__(self, name):
        super().__init__(name)
        self.current_data = pd.DataFrame()
        self.current_row = pd.DataFrame()

    def create_row(self, dict):
        self.current_row = pd.DataFrame(data=[dict])
        self.current_data = pd.concat([self.current_data, self.current_row], ignore_index=True)

    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []

        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                if isinstance(card, ColorCard) and not isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        special_card = ColorCard()
                        special_card.change_color(color)
                        valid_cards_to_put.append(special_card)
                elif isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        special_card = Plus4Card()
                        special_card.change_color(color)
                        valid_cards_to_put.append(special_card)
                else:
                    valid_cards_to_put.append(card)
        return valid_cards_to_put

    def valid_cards(self, card_taken=None) -> list:
        """Creates a list of cards that can be played. If there isn't any, puts DrawCard()"""
        valid_cards = []
        if card_taken is not None:
            if isinstance(card_taken, ColorCard):
                for color in self.possible_colors:
                    valid_cards.append(self.create_card_instance(card_taken.value, color))
                return valid_cards
            return [card_taken]

        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            valid_cards.append(StopCard("Stop", "Stop"))
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards = self.collect_valid_cards_of_given_instance(
                Plus2Card) + self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        valid_cards = self.collect_valid_cards_of_given_instance(Card)

        return valid_cards if len(valid_cards) > 0 else [DrawCard()]

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        most_colors = sorted(self.hand, key=lambda card_in_hand: card_in_hand.color)
        for card in most_colors:
            if card.color in possible_colors:
                return card.color
        return random.choice(possible_colors)

    def show_card_list(self, list_of_cards):
        cards_str = "| "
        for card in list_of_cards:
            cards_str += str(card) + " | "
        return cards_str

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
            card = Card("None", "None")
        else:
            card = Card(card_value, card_color)
        return card

    def bot_reset(self):
        pass