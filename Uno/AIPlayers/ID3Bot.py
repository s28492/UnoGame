import random
import os
import pickle

from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.DecisionTrees.ID3Tree import ID3Tree
from Uno.DecisionTrees.C4_5Tree import C4_5Tree
from Uno.game.Card import *



class ID3Bot(BaseAIBot):
    """
    Represents an AI bot for playing UNO that utilizes an ID3 decision tree.
    """
    def __init__(self, name: str
                 , tree_file: str = None
                 , tree_instance = None):
        """
        Initializes the ID3Bot with a name and decision tree.

        Parameters:
            name (str): The name of the bot.
            tree_file (str, optional): The file path to a serialized ID3 decision tree. Defaults to None.
            tree_instance (ID3Tree, optional): An instance of an ID3Tree. Defaults to None.

        If neither `tree_file` nor `tree_instance` is provided, a default tree is loaded.
        """
        super().__init__(name)
        if tree_file is not None:
            self.id_tree: ID3Tree = load_tree(tree_file)
        elif tree_instance is not None:
            self.id_tree = tree_instance
        else:
            self.id_tree: ID3Tree = load_tree(
                "Uno/DecisionTrees/20240801_2159_improved_7_nodes_deep_decoded_target_values_tree.pkl")



    def move(self, first_card_taken=None, game=None):
        """
        Determines the bot's move based on the current game state and the ID3 decision tree.

        Parameters:
            first_card_taken (Card, optional): The first card taken during the bot's turn. Defaults to None.

        Returns:
            Card: The card selected by the bot to play.
        """

        valid_cards: list = self.valid_cards(card_taken=first_card_taken)
        if len(valid_cards) == 1 and not isinstance(valid_cards[0], ColorCard):
            return valid_cards[0]
        node_values = self.id_tree.predict(self.current_row)
        for predicted_card in node_values.index.to_list():
            splitted_index = predicted_card.split(" ")
            if len(splitted_index) == 1:
                card = self.create_card_instance(splitted_index[0])
            else:
                card = self.create_card_instance(splitted_index[0], splitted_index[1])
            if card in valid_cards:
                return card
        card = random.choice(valid_cards)
        if isinstance(card, ColorCard):
            card.change_color(self.choose_color())
        return card

    def bot_reset(self):
        """
        Resets the bot's ID3 tree instance, preparing it for reuse or reinitialization.
        """
        self.id_tree: None
        self.id_tree = None
        self.id_tree: ID3Tree = None

def load_tree(filename):
    """
    Loads a serialized ID3 decision tree from a file.

    Parameters:
        filename (str): The path to the file containing the serialized tree.

    Returns:
        ID3Tree: The deserialized ID3 decision tree instance.
    """
    abs_path = os.path.abspath(filename)
    with open(abs_path, 'rb') as f:
        return pickle.load(f)
