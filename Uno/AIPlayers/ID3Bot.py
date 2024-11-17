import random
import os
import pickle

from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.ID3Tree import ID3Tree
from Uno.game.Card import *


class ID3Bot(BaseAIBot):
    def __init__(self, name: str
                 , tree_file: str = None
                 , tree_instance = None):
        super().__init__(name)

        if tree_file is not None:
            self.id_tree: ID3Tree = load_tree(tree_file)
        elif tree_instance is not None:
            self.id_tree = tree_instance
        else:
            self.id_tree: ID3Tree = load_tree(
                "/Uno/DecisionTrees/20240727_1631_id_tree.pkl")




    def move(self, first_card_taken=None):

        valid_cards: list = self.valid_cards(card_taken=first_card_taken)
        if len(valid_cards) == 1 and not isinstance(valid_cards[0], ColorCard):
            return valid_cards[0]
        node_values = self.id_tree.predict(self.current_row).value_counts(sort=True)
        # if self.name == "LaterId3Bot2":
        #     print(node_values)
        #     print(self.show_card_list(valid_cards))
        for index_card in node_values.index.to_list(): # dla każdej karty z bazy danych tworzy instancję
            # if self.name == "LaterId3Bot2":
            #     print("MMMMMMMMMMMMMM")
            #     print(f"Index card type: {type(index_card)}")
            splitted_index = index_card[0].split(" ")
            # if self.name == "LaterId3Bot2":
            #     print(splitted_index)
            if len(splitted_index) == 1:
                card = self.create_card_instance(splitted_index[0])
            else:
                card = self.create_card_instance(splitted_index[0], splitted_index[1])
            # if self.name == "LaterId3Bot2":
            #     print(card)
            #     print(card in valid_cards)
            if card in valid_cards:
                # if self.name == "PreviousID3Bot":
                #     print("BBBBBBBBBBBBBBBBBB")
                return card
        card = random.choice(valid_cards)
        if isinstance(card, ColorCard):
            card.change_color(self.choose_color())
        # if self.name == "PreviousID3Bot":
        #     print("AAAAAAAAAAAAAAAA")
        return card

    def bot_reset(self):
        self.id_tree: None
        self.id_tree = None
        self.id_tree: ID3Tree = None

def load_tree(filename):
    abs_path = os.path.abspath(filename)
    with open(abs_path, 'rb') as f:
        return pickle.load(f)
