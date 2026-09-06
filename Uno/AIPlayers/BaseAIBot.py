import pandas as pd
import random
import os
import pickle
import sys
from Uno.game.Card import ColorCard, Plus4Card, StopCard, DrawCard, Plus2Card, Card, ReverseCard
from Uno.players.Bot import Bot


class BaseAIBot (Bot):
    def __init__(self, name):
        super().__init__(name)
        self.current_data = pd.DataFrame()
        self.current_row = pd.DataFrame()

    def create_row(self, data_dict):
        self.current_row = pd.DataFrame(data=[data_dict])
        self.current_data = pd.concat([self.current_data, self.current_row], ignore_index=True)
        
    def show_card_list(self, list_of_cards):
        cards_str = "| "
        for card in list_of_cards:
            cards_str += str(card) + " | "
        return cards_str

    def create_color_cards(self, plus_card: bool = False) -> list:
        cards = []
        if plus_card:
            for color in ["Red", "Green", "Blue", "Yellow"]:
                card = Plus4Card()
                card.change_color(color)
                cards.append(card)
        else:
            for color in ["Red", "Green", "Blue", "Yellow"]:
                card = ColorCard()
                card.change_color(color)
                cards.append(card)
        return cards

    def bot_reset(self):
        pass