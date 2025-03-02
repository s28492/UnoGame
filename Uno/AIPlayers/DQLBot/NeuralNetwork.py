import os
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self, in_features=206, h1=128, h2=64, out_features=62, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, out_features)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)
        return x

    def initialize_parameters(self):
        W1 = np.random.randn(10, 16)
        b1 = np.random.randn(10, 1)
        W2 = np.random.randn(10, 10)
        b2 = np.random.randn(10, 1)
        return W1, b1, W2, b2

    # (num_red, num_green, num_blue, num_yellow, num_stop, num_plus2, num_plus4, num_all_color, num_cards_left_in_deck, round,
    #  num_enemy_cards, direction, num_colors_in_hand, num_cards_in_hand)