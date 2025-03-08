import numpy as np
from Uno.game.GameState import GameState
from Uno.game.Card import Card
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.DQLBot.NeuralNetworkModel import NeuralNetworkModel

class DQLBot(BaseAIBot):
    color_multiplayer = {"Red":0, "Green":13, "Blue":26, "Yellow":39, "Colors": 39}
    values_multiplayer = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "Stop": 10, "Reverse": 11, "+2": 12, "All": 13, "+4": 14
    }
    def __init__(self, name, main_network):
        super().__init__(name)
        self.__main_network: NeuralNetworkModel = main_network
        self.__target_network: NeuralNetworkModel = NeuralNetworkModel()
        self.__target_network.load_weights(self.__main_network.state_dict())
        self._epsilon = 1

        # Order: RGBY -> 0:9, stop_card, reverse_card, +2_card, all_colors, +4_colors
        self.cards_in_hand = np.zeros([54])
        # 20 values + 4 colors
        self.card_on_top_color = np.zeros([5])
        self.card_on_top_value = np.zeros([15])
        # num_colors_in_hand ...
        self.additional_info = np.zeros([14])
        # Order: 21 values + 4 colors + StopStop + Draw
        self.previous_moves1 = np.zeros([27])
        self.previous_moves2 = np.zeros([27])
        self.previous_moves3 = np.zeros([27])
        self.previous_moves4 = np.zeros([27])

    def collect_card_values(self):
        pass

    def collect_card_colors(self):
        pass

    def collect_history(self):
        pass

    def collect_data(self):
        pass

    def collect_cards_in_hand(self):
        for card in self.cards_in_hand:
            card_place = DQLBot.color_multiplayer[card.color] + DQLBot.values_multiplayer[card.value]
            self.cards_in_hand[card_place] += 1

    def fill_card_on_top(self, game_state: GameState):
        card_on_top: Card = self.game_state_copy.get_card_on_top()
        self.card_on_top_color[
            (DQLBot.color_multiplayer[card_on_top.get_color()]) / 13
        ] += 1
        self.card_on_top_value[
            (DQLBot.values_multiplayer[card_on_top.get_value()])
        ] +=1

    def move(self, first_card_taken=None, game=None):
        pass



