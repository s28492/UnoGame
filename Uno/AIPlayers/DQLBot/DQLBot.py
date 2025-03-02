import random
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.DQLBot.NeuralNetworkModel import NeuralNetworkModel

class DQLBot(BaseAIBot):
    def __init__(self, name, main_network):
        super().__init__(name)
        self.main_network: NeuralNetworkModel = main_network
        self.target_network: NeuralNetworkModel = NeuralNetworkModel()
        self.target_network.load_weights(self.main_network.state_dict())
        self.epsilon = 1

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



