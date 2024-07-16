import pandas as pd
from Uno.DecisionTrees.ID3Tree import ID3Tree, load_tree, decode_columns
from Uno.players.Bot import Bot
from Uno.game.Card import *
import random
import os
class ID3Bot(Bot):
    def __init__(self, name:str
                 , tree_file:str="/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/DecisionTrees/20240716_2005_id_tree.pkl"):
        super().__init__(name)
        self.current_data = pd.DataFrame()
        self.current_row = pd.DataFrame()
        self.id_tree: ID3Tree = load_tree(tree_file)

    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                if isinstance(card, ColorCard) and not isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        valid_cards_to_put.append(ColorCard(color, card.color))
                elif isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        valid_cards_to_put.append(Plus4Card(color, card.color))
        return valid_cards_to_put

    def valid_cards(self, card_taken = None) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        valid_cards = []
        if card_taken is not None:
            return [card_taken, DrawCard()]

        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            valid_cards.append(StopCard("Stop", "Stop"))
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            valid_cards.append(DrawCard())
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus2Card) + self.collect_valid_cards_of_given_instance(Plus4Card)
            valid_cards.append(DrawCard())
            return valid_cards

        valid_cards = self.collect_valid_cards_of_given_instance(Card)
        valid_cards.append(DrawCard())

        return valid_cards

    def create_row(self, dict):
        self.current_row = pd.DataFrame(data=[dict])
        self.current_data = pd.concat([self.current_data, self.current_row], ignore_index=True)


    def filter_cards_from_hand(self, node):
        cards_occurences_dict = {}
        for card in self.hand:
            if not isinstance(card, ColorCard):
                if card not in cards_occurences_dict:
                    cards_occurences_dict[card] = 1
                else:
                    cards_occurences_dict[card] += 1
            elif isinstance(card, Plus4Card):
                pass

    def card_in_current_node_amoount(self, cards, node):
        for card in cards:
            if isinstance(card, Plus4Card):
                pass

    def move(self, first_card_taken=None):
        self.console.print(self.show_hand())
        valid_cards = self.valid_cards(card_taken=first_card_taken)
        node_values = self.id_tree.predict(self.current_row).value_counts(sort=True)
        for index_card in node_values.index.to_list():
            card = self.create_card_instance(index_card)
            if card in valid_cards:
                if isinstance(card, ColorCard):
                    card.change_color(self.choose_color())
                print(f"Card in loop {card}")
                return card
        card = random.choice(valid_cards)
        if isinstance(card, ColorCard):
            card.change_color(self.choose_color())
        self.console.print(f"Card in the end {card}")
        return card

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        most_colors = sorted(self.hand, key=lambda card_in_hand: card_in_hand.color)
        for card in most_colors:
            if card.color in possible_colors:
                return card.color
        return random.choice(possible_colors)
    def create_card_instance(self, card_value: str):
        card_value = card_value.split(" ")
        if card_value[0] == "+4":
            card = Plus4Card(card_value[0], card_value[1])
        elif card_value[0] == "All":
            card = ColorCard(card_value[0], card_value[1])
        elif card_value[0] == "Stop" and len(card_value) == 1:
            card = StopCard(card_value[0], card_value[0])
        elif card_value[0] == "Stop" and len(card_value) == 2:
            card = StopCard(card_value[0], card_value[1])
        elif card_value[0] == "+2":
            card = Plus2Card(card_value[0], card_value[1])
        elif card_value[0] == "Reverse":
            card = ReverseCard(card_value[0], card_value[1])
        elif card_value[0] == "Draw":
            card = DrawCard()
        else:
            card = Card(card_value[0], card_value[1])
        return card