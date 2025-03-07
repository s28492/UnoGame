import random
import numpy as np
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.DQLBot.NeuralNetworkModel import NeuralNetworkModel

class DQLBot(BaseAIBot):
    def __init__(self, name, main_network):
        super().__init__(name)
        self.main_network: NeuralNetworkModel = main_network
        self.target_network: NeuralNetworkModel = NeuralNetworkModel()
        self.target_network.load_weights(self.main_network.state_dict())
        self.epsilon = 1

        # Order: RGBY -> 0:9, stop_card, reverse_card, +2_card, all_colors, +4_colors
        self.in_60_cards = np.array([60])
        # 20 values + 4 colors
        self.card_on_top = np.array([24])
        # num_colors_in_hand ...
        self.additional_info = np.array([14])
        # Order: 21 values + 4 colors + StopStop + Draw
        self.previous_moves1 = np.array([27])
        self.previous_moves2 = np.array([27])
        self.previous_moves3 = np.array([27])
        self.previous_moves4 = np.array([27])

    def collect_card_values(self):
        pass

    def collect_card_colors(self):
        pass

    def collect_history(self):
        pass

    def collect_data(self):
        pass

    def move(self, **kwargs):

        pass



