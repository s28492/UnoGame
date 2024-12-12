import os
import random

import pandas as pd

from Uno.DecisionTrees.ID3Tree import ID3Tree
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.DecisionTrees.ID3Tree import load_tree


class C4_5BaggingEnsebleBot(BaseAIBot):
    def __init__(self, name, source_folder):
        super().__init__(name)
        self.source_folder = source_folder
        self.trees: list[ID3Tree] = []
        self.collect_trees()
        self.all_cards = pd.Series(data=[0] * 62, index=[
            '1 Blue', '8 Blue', '8 Green', '+2 Green', '4 Green',
            '9 Green', '+4 Blue', '5 Blue', 'Stop Blue', '2 Blue',
            'All Red', '3 Red', '6 Red', '1 Yellow', 'Stop Yellow',
            'Reverse Yellow', '6 Yellow', '8 Yellow', '8 Red', '5 Red',
            '9 Red', '9 Blue', '5 Green', '6 Green', 'Reverse Red', 'All Blue',
            'Reverse Blue', '+2 Blue', '+4 Yellow', '4 Blue', 'Reverse Green',
            '3 Blue', 'Stop Red', '4 Red', '2 Red', '2 Yellow', '5 Yellow',
            '1 Red', '2 Green', '7 Green', 'All Yellow', '0 Yellow',
            '3 Yellow', '9 Yellow', '4 Yellow', 'Stop Green', '3 Green',
            '7 Yellow', '7 Blue', '1 Green', '0 Red', '+2 Yellow', '6 Blue',
            'All Green', '7 Red', '+2 Red', '+4 Red', '+4 Green', '0 Green',
            '0 Blue', 'All Colors', '+4 Colors'
        ], dtype=float)

    def object_to_text(self, cards_list):
        new_list = []
        for card in cards_list:
            new_list.append(card.__str__())
        return new_list

    def move(self, first_card_taken=None):
        # print("========================================")
        valid_cards = self.valid_cards(first_card_taken)
        # print("A len of valid cards: ", len(valid_cards))
        if len(valid_cards) == 1:
            # print("Card returned from condition: ", valid_cards[0].__str__())
            return valid_cards[0]
        valid_cards = self.object_to_text(valid_cards)

        # print("B Valid cards: ", valid_cards)

        for tree in self.trees:
            node_values = tree.predict(self.current_row).value_counts(sort=True)

            if isinstance(node_values.index, pd.MultiIndex):
                node_values.index = node_values.index.get_level_values(0)
            filtered_node_values = node_values[node_values.index.isin(valid_cards)]

            tree_data = filtered_node_values / node_values.sum()


            for index in tree_data.index:
                self.all_cards.loc[index] += tree_data[index]

        self.all_cards.sort_values(inplace=True, ascending=False)
        if self.all_cards.loc[self.all_cards.index.tolist()[0]] != 0:
            card_to_play = self.all_cards.index.tolist()[0].split(" ")
        else:
            card_to_play = random.choice(valid_cards).split(" ")
        # print(f"card_to_play: {card_to_play}")
        # time.sleep(2)
        if len(card_to_play) == 1:
            card = self.create_card_instance(card_to_play[0])
        else:
            card = self.create_card_instance(card_to_play[0], card_to_play[1])

        # Reset all_cards for the next move
        # print(f"All cards: {self.all_cards}")
        self.all_cards[:] = 0
        # print("Cards in hand: ", len(self.hand))
        # print("Cards to take: ", self.cards_to_take)
        # print("Turns to stop: ", self.turns_to_stop)
        # print("Card on top: ", self.card_on_top)
        # print("valid_cards ", valid_cards)
        # print(f"card {type(card)} --> {card.__str__()}\n")
        # time.sleep(0.2)
        return card

    def collect_trees(self):
        for root, dirs, files in os.walk(self.source_folder, topdown=True):
            for name in files:
                full_path = os.path.join(root, name)
                tree: ID3Tree = load_tree(full_path)
                tree.decode_target_values()
                self.trees.append(tree)

    def bot_reset(self):
        self.players = None
        self.pile = None
        self.card_on_top = None
        self.direction = None
        self.turns_to_stop = None
        self.cards_to_take = None
        self.stop_cards = []
        self.plus_2_cards = []
        self.plus_4_cards = []

if __name__ == '__main__':
    bagging_bot = C4_5BaggingEnsebleBot(source_folder='Uno/DecisionTrees/BaggingTrees/n10_d1_sp0.63_dseTrue')
