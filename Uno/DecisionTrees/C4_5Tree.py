import numpy
import pandas as pd
import numpy as np


class C4_5Tree:

    def __init__(
            self, X_data: np.array, Y_data: np.array, remaining_data_indices: np.array = None,
            remaining_column_indices: np.array = None, labels_encodes: dict = None, parent: C4_5Tree = None,
            node_depth: int = None, is_leaf: bool = False
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
        self.children = []
        self.is_leaf = is_leaf
        self.node_depth = node_depth

    def calculate_entropy(self, indexes):
        # Entropy(S) = - ( Sum(P * log_2 (P))
        entropy = 0

        _, counts = np.unique(self.Y_data[indexes], return_counts=True)
        for count in counts:
            p = count / self.Y_data[indexes].shape[0]
            entropy -= p * np.log2(p)
        return entropy

    def calculate_information_gain_for_column(self, column_index: int, current_entropy) -> tuple:
        # Column values for the current subset
        x_column = self.X_data[:, column_index]
        x_column_values, counts = np.unique(x_column[self.remaining_data_indices], return_counts=True)
        split_indexes = []
        values_from_splitted_indexes = []

        partial_entropy = 0
        for x_column_value, count in zip(x_column_values, counts):
            proportion_of_given_value_in_column = count / self.remaining_data_indices.shape[0]

            # Mapping filtered indexes values to remaining_data_indices for data alignment
            indexes_of_given_value = self.remaining_data_indices[
                np.where(x_column[self.remaining_data_indices] == x_column_value)[0]
            ]
            values_from_splitted_indexes.append(x_column_value)
            split_indexes.append(indexes_of_given_value)
            # Calculating partial entropy
            partial_entropy += proportion_of_given_value_in_column*self.calculate_entropy(indexes_of_given_value)

        return current_entropy - partial_entropy, values_from_splitted_indexes ,split_indexes

    def calculate_split_information_for_column(self, column_index: int):
        split_information = 0
        x_column = self.X_data[:, column_index]
        _, counts = np.unique(x_column[self.remaining_data_indices], return_counts=True)
        for count in counts:
            proportion_of_value = count / self.remaining_data_indices.shape[0]
            split_information -= proportion_of_value * np.log2(proportion_of_value)
        return split_information

    def calculate_best_gain_ratio(self) -> tuple:
        gain_ratios = []
        all_split_values = []  # Collects split values for each column
        all_split_indexes = []  # Collects indexes for each split
        # Current entropy for the entire dataset
        current_entropy = self.calculate_entropy(self.remaining_data_indices)

        # Adds all columns' information gains to an array
        for column_index in self.remaining_column_indices:
            information_gain, split_values, split_indexes = self.calculate_information_gain_for_column(column_index,
                                                                                                       current_entropy)
            split_information = self.calculate_split_information_for_column(column_index)
            gain_ratio = information_gain / split_information

            gain_ratios.append(gain_ratio)
            all_split_values.append(split_values)
            all_split_indexes.append(split_indexes)

        # Convert information gains to numpy array for efficient operations
        gain_ratios = np.array(gain_ratios)

        # Find the best column
        best_column_idx = np.argmax(gain_ratios)
        # Adjust best index to reference "remaining_column_indexes" not "indormation_gains"
        best_column_index = self.remaining_column_indices[best_column_idx]
        best_split_values = np.array(all_split_values[best_column_idx])
        best_split_indexes = np.array(all_split_indexes[best_column_idx])

        max_gain_ratio = gain_ratios[best_column_idx]
        return best_column_index, max_gain_ratio, best_split_values, best_split_indexes




    def build_tree(self, max_depth: int, min_values_per_leaf: int, min_information_gain: float) ->'C4_5Tree':
        best_column_index, max_gain_ratio, best_split_values, best_split_indexes = self.calculate_best_gain_ratio()


        if (self.node_depth == max_depth) or (max_gain_ratio < min_information_gain):
            self.is_leaf = True
            return self

        for i in range(0, best_split_values.shape[0]):
            is_enough_data_in_node: bool = best_split_indexes[i].shape[0] >= min_values_per_leaf
            if is_enough_data_in_node:
                new_node = C4_5Tree(self.X_data, self.Y_data, remaining_data_indices=best_split_indexes[i],
                                    remaining_column_indices=best_split_indexes[i], labels_encodes=self.labels_encodes,
                                    parent=self, node_depth=self.node_depth+1)
                self.children.append(new_node)
                new_node.build_tree(max_depth, min_values_per_leaf, min_information_gain)

        return self





































