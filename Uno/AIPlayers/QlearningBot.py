import numpy as np

from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.game.Card import DrawCard


class QlearningBot(BaseAIBot):
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0,
                 epsilon_decay=0.9999, min_epsilon=0.01,
                 num_episodes=100000):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.num_episodes = num_episodes

    def valid_actions(self, card_taken=None):
        valid_actions = []
        valid_actions.append(self.valid_cards(card_taken))
        if self.turns_to_stop == 0:
            valid_actions.append(DrawCard())
        return valid_actions
        

    def move(self, first_card_taken=None, game=None):
        pass