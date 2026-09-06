from numpy.f2py.auxfuncs import throw_error

from Uno.NeuralNetwork import *
from Uno.NeuralNetwork.neural_network import NeuralNetwork
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.NeuralNetwork.ModelWithLabels import ModelWithLabels, Model
from Uno.games_data.dataHandler import  encode_data_with_label, load_pickle
from Uno.game.Card import *
from src.utils import get_project_root

import torch
import numpy as np
import random
import os
import pickle


class SimpleNNBot(BaseAIBot):

    def __init__(self, name = "SimpleNNBot", model_with_labels=None, model_url=None):
        super().__init__(name)
        if model_with_labels is not None:
            self.model = model_with_labels
        elif model_url is not None:
            self.model = load_pickle(model_url)
        else:
            print("Wrong model source provided")

    def predict_card(self):
        row_encoded_df = encode_data_with_label(self.current_row, self.model.get_labels())
        data = torch.FloatTensor(row_encoded_df.to_numpy())
        with torch.no_grad():
            y_pred = self.model.get_model().forward(data)
            y_pred_numpy = y_pred.detach().numpy()

            indices = np.arange(y_pred_numpy.size)
            array_2d = np.column_stack([indices, y_pred_numpy[0]])
            array_2d = array_2d[array_2d[:, 1].argsort()][-1:0:-1]


        return array_2d

    def move(self, first_card_taken=None, game=None):
        valid_cards: list = self.valid_cards(first_card_taken)
        if len(valid_cards) == 1 and not isinstance(valid_cards[0], ColorCard):
            return valid_cards[0]


        predicted_values = self.predict_card()
        for values in predicted_values:
            card_str = self.model.get_labels()["card_played"][int(values[0])]
            card_list = card_str.split(' ')
            card = self.create_card_instance(card_list[0], card_list[1])

            if card in valid_cards:
                return card
        card = random.choice(valid_cards)
        if isinstance(card, ColorCard):
            card.change_color(self.choose_color())
        return card

