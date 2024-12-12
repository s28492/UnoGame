import pandas as pd
import numpy as np
import multiprocessing as mp
from numba import njit
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.game.Card import ColorCard, Plus4Card
from Uno.DecisionTrees.ID3Tree import encode_data_with_label


class NaiveBayesianBot(BaseAIBot):
    def __init__(self, name, data: pd.DataFrame, labels_to_decode):
        super().__init__(name)
        self.data = data
        self.lock = mp.Lock()
        self.all_labels_to_decode = labels_to_decode
        self.target_label_to_encode = {value: key for key, value in self.all_labels_to_decode['card_played'].items()}
        pd.set_option('future.no_silent_downcasting', True)

    def move(self, first_card_taken=None):
        valid_cards = self.valid_cards(card_taken=first_card_taken)
        valid_cards = self.append_colors(valid_cards)

        if len(valid_cards) == 1 and not isinstance(valid_cards[0], ColorCard):
            return valid_cards[0]
        valid_cards = [self.target_label_to_encode[str(card)] for card in valid_cards]
        filtered_data: pd.DataFrame = self.filter_data(valid_cards)
        card_probability_overall = filtered_data["card_played"].value_counts() / filtered_data.shape[0]

        refactored_row = self.current_row.loc[:, self.data.columns.to_list()[:-1]]
        refactored_row = encode_data_with_label(refactored_row, self.all_labels_to_decode)
        # print(f"Current row: {refactored_row.columns}")
        # print(f"Current row: {self.data.columns}")
        max_probability = 0
        best_card = None
        for card in card_probability_overall.index:
            probabiliies_to_multiply = []
            given_card_data: pd.DataFrame = filtered_data.loc[filtered_data["card_played"] == card]

            numpy_probability = calculate_naive_bayes(refactored_row.to_numpy(), given_card_data.to_numpy(),
                                                      card_probability_overall[card])

            # for column in refactored_row.columns.to_list():
            #     value = refactored_row[column].iloc[-1]
            #     count_value_given_card = given_card_data[given_card_data[column] == value].shape[0]
            #     probabiliies_to_multiply.append(count_value_given_card / given_card_data.shape[0])
            # product = np.prod(probabiliies_to_multiply) * card_probability_overall[card]

            # print(f"before comparing probability: \nCard: {card}\nProduct:{product}max:prob:{max_probability}")
            if numpy_probability >= max_probability:
                max_probability = numpy_probability
                best_card = card

        # print(f"Before for loop. Valid cards: {valid_cards}")
        # print(f"Best card -> {self.all_labels_to_decode['card_played'][best_card]}")
        best_card = self.all_labels_to_decode['card_played'][best_card].split(" ")
        best_card = self.create_card_instance(best_card[0]) if len(best_card) == 1 \
            else self.create_card_instance(best_card[0], best_card[1])
        return best_card

    def append_colors(self, card_list):
        new_card_list = card_list.copy()
        for card in new_card_list:
            if isinstance(card, Plus4Card):
                card_list.remove(card)
                for color in self.possible_colors:
                    instance = Plus4Card()
                    instance.change_color(color)
                    card_list.append(instance)

            elif isinstance(card, ColorCard):
                card_list.remove(card)
                for color in self.possible_colors:
                    instance = ColorCard()
                    instance.change_color(color)
                    card_list.append(instance)
        return card_list

    def filter_data(self, valid_cards):
        valid_string_cards: list = [card for card in valid_cards]
        filtered_data = self.data.loc[self.data["card_played"].isin(valid_string_cards)]
        return filtered_data

    def calculate_naive_bayes(self, card):
        pass
    def bot_reset(self):
        self.data = None
        self.lock = mp.Lock()
        self.all_labels_to_decode = None
        self.target_label_to_encode = None

@njit(nogil=True)
def calculate_naive_bayes(numpy_current_row: np.array, numpy_data: np.array, probability_of_target_attribute: float):
    num_of_samples = numpy_data.shape[0]
    num_of_features = numpy_data.shape[1] - 1

    data_to_multiply = np.zeros(num_of_features)

    for i in range(num_of_features):
        occurrences = numpy_data[:, i] == numpy_current_row[0][i]
        number_of_occurrences = np.sum(occurrences)
        partial_probability_value = number_of_occurrences / num_of_samples if number_of_occurrences != 0 else 1 / np.sum(np.unique(numpy_data[:, i]))
        data_to_multiply[i] = partial_probability_value

    final_probability = np.prod(data_to_multiply) * probability_of_target_attribute
    return final_probability
