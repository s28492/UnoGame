import numpy
import pandas as pd
import numpy as np


class C4_5Tree:

    def __init__(
            self, X_data: np.array, Y_data: np.array, remaining_data_indices: np.array = None,
            remaining_column_indices: np.array = None, labels_encodes: dict = None, parent: C4_5Tree = None,
            node_depth: int = None
                 ):
        self.X_data = X_data
        self.Y_data = Y_data
        if remaining_data_indices is None:
            self.remaining_data_indices: np.array = np.arange(Y_data.shape[0])
        else:
            self.remaining_data_indices:np.array = remaining_data_indices

        if remaining_column_indices is None:
            self.remaining_column_indices:np.array = np.arange(X_data.shape[1])
        else:
            self.remaining_column_indices:np.array = remaining_column_indices
        self.labels_encodes = labels_encodes
        self.parent = parent
        self.node_depth = node_depth

    # def calculate_column_entropy(self, column_index: int) -> float:
    #     # Entropy(S) = - ( Sum(P * log_2 (P))
    #     entropy = 0.0
    #     X_column = self.X_data[self.remaining_data_indices, column_index]
    #     unique_X_data = np.unique(X_column, return_counts=True)
    #     # Iterate through each value in X column
    #     for i, uniqie_X in enumerate(unique_X_data):
    #         # Create list of indexes containing given value
    #         indexes = np.where(X_column == uniqie_X[i])[0]
    #         # Iterate through each value in Y column
    #         for _, counted in np.unique(self.Y_data[indexes], return_counts=True):
    #             p = counted[i] / indexes.shape[0]
    #             partial_entropy = (p * np.log2(p))
    #             entropy -= partial_entropy
    #     return entropy

    def calculate_entropy(self, indexes):
        # Entropy(S) = - ( Sum(P * log_2 (P))
        entropy = 0
        
        _, counts = np.unique(self.Y_data[indexes], return_counts=True)
        for count in counts:
            p = count / self.Y_data[indexes].shape[0]
            entropy -= p * np.log2(p)
        return entropy

    def calculate_information_gain_for_column(self, column_index: int, current_entropy) -> float:
        # Column values for the current subset
        x_column = self.X_data[:, column_index]
        x_column_values, counts = np.unique(x_column[self.remaining_column_indices], return_counts=True)

        partial_entropy = 0
        for x_column_value, count in zip(x_column_values, counts):
            proportion_of_given_value_in_column = count / self.remaining_column_indices.shape[0]

            # Mapping filtered indexes values to remaining_column_indices for data alignment
            indexes_of_given_value = self.remaining_column_indices[
                np.where(x_column[self.remaining_column_indices] == x_column_value)[0]
            ]
            # Calculating partial entropy
            partial_entropy += proportion_of_given_value_in_column*self.calculate_entropy(indexes_of_given_value)

        return current_entropy - partial_entropy

    def calculate_best_information_gain(self) -> tuple:
        information_gains = []
        # Current entropy for the entire dataset
        current_entropy = self.calculate_entropy(self.remaining_column_indices)
        # Adds all columns information gains to array
        for column_index in self.remaining_column_indices:
            information_gain = self.calculate_information_gain_for_column(column_index, current_entropy)
            information_gains.append(information_gain)

        information_gains = np.array(information_gains)

        best_column_index = self.remaining_column_indices[np.argmax(information_gains)]
        max_information_gain = information_gains[best_column_index]
        return best_column_index, max_information_gain




    def build_tree(self, max_depth: int, min_values_per_leaf: int, min_information_gain: float) -> C4_5Tree:
        best_gain_ratio, best_attribute, renaining_data_indices = self.best_information_gain()