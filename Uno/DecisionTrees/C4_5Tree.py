import numpy
import pandas as pd
import numpy as np
import datetime
import pickle
import time

from multiprocessing import Pool, cpu_count, freeze_support
from Uno.games_data.dataHandler import *


class C4_5Tree:

    def __init__(
            self, X_data: np.array, Y_data: np.array, remaining_data_indices: np.array = None,
            remaining_column_indices: np.array = None, labels_encodes: dict = None, parent: 'C4_5Tree' = None,
            node_depth: int = 0, is_leaf: bool = False, node_value: str = None, split_attribute: int = None
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
        self.node_value = node_value
        self.split_attribute = split_attribute

    def get_labels(self):
        return self.labels_encodes

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
        # print("Col index ", column_index)
        # print("Col index type ", type(column_index))
        # print("Columns left ", self.remaining_column_indices)
        # print("Column of column index ", self.remaining_column_indices[column_index])
        # print("X Data ", self.X_data)
        # print("X Data type", type(self.X_data))
        # print("X Data values", self.X_data.iloc[:, column_index])
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

    def find_best_split(self, column_index, current_entropy):
        information_gain, split_values, split_indexes = \
            self.calculate_information_gain_for_column(column_index, current_entropy)
        split_information = self.calculate_split_information_for_column(column_index)
        return information_gain, split_values, split_indexes, split_information

    def calculate_best_gain_ratio(self) -> tuple:
        current_entropy = self.calculate_entropy(self.remaining_data_indices)

        # Parallel processing: each column’s best split
        with Pool(cpu_count()) as pool:
            results = pool.starmap(
                self.find_best_split,
                [(col_idx, current_entropy) for col_idx in self.remaining_column_indices]
            )

        gain_ratios = []
        all_split_values = []
        all_split_indexes = []

        for (information_gain, split_values, split_indexes, split_information) in results:
            if split_information == 0:
                gain_ratio = 0
            else:
                gain_ratio = information_gain / split_information

            gain_ratios.append(gain_ratio)
            all_split_values.append(split_values)
            all_split_indexes.append(split_indexes)

        gain_ratios = np.array(gain_ratios)

        # Find the index of the best gain ratio
        best_idx = np.argmax(gain_ratios)
        best_gain_ratio = gain_ratios[best_idx]

        best_column_index = self.remaining_column_indices[best_idx]
        best_split_values = np.array(all_split_values[best_idx])
        best_split_indexes = all_split_indexes[best_idx]

        return best_column_index, best_gain_ratio, best_split_values, best_split_indexes


    def build_tree(self, max_depth: int, min_values_per_leaf: int, min_gain_ratio: float) -> 'C4_5Tree':
        # Calculating the best split based on gain ratio
        best_column_index, max_gain_ratio, best_split_values, best_split_indexes = self.calculate_best_gain_ratio()

        self.split_attribute = best_column_index

        # Checking stopping conditions
        max_depth_reached = self.node_depth == max_depth
        min_gain_ratio_reached = max_gain_ratio < min_gain_ratio
        is_data_pure = np.unique(self.Y_data[self.remaining_data_indices]).shape[0] == 1
        one_column_left = self.remaining_column_indices.shape[0] == 1
        if max_depth_reached or min_gain_ratio_reached or is_data_pure or one_column_left:
            self.is_leaf = True
            return self

        # Updating remaining_column_indices for children
        child_remaining_columns = self.remaining_column_indices[self.remaining_column_indices != best_column_index]

        self.show_tree_building_process()

        for i in range(0, best_split_values.shape[0]):
            child_data_indices = np.array(best_split_indexes[i])
            is_enough_data_in_node: bool = child_data_indices.shape[0] >= min_values_per_leaf
            if is_enough_data_in_node:
                new_node = C4_5Tree(
                    X_data=self.X_data,
                    Y_data=self.Y_data,
                    remaining_data_indices=child_data_indices,
                    remaining_column_indices=child_remaining_columns,
                    labels_encodes=self.labels_encodes,
                    parent=self,
                    node_depth=self.node_depth + 1,
                    node_value=best_split_values[i]
                )
                self.children.append(new_node)
                new_node.build_tree(max_depth, min_values_per_leaf, min_gain_ratio)

        return self



    def predict_from_df(self, data_to_predict: pd.DataFrame):
        columns = np.array(data_to_predict.columns.shape[0])
        encoded_data = encode_data_with_label(data_to_predict, self.labels_encodes)

        if self.is_leaf:
            cards, counts = np.unique(self.Y_data[self.remaining_data_indices], return_counts=True)
            output_series = pd.Series(data=dict(zip(cards, counts)), name="card_played").sort_values(ascending=False)
            return output_series

        for child in self.children:
            if child.node_value == encoded_data[child.split_attribute].iloc[0]:
                return child.predict_from_df(data_to_predict)


    def save_tree(self, filename, is_temporary=False, directory=""):
        """
        Saves the tree to a file using pickle.

        Parameters:
            filename (str): The name of the file to save the tree.
            is_temporary (bool, optional): Whether the file is temporary. Defaults to False.
            directory (str, optional): The directory to save the file. Defaults to "".

        Returns:
            str: The full path of the saved file.
        """
        if is_temporary:
            filename = "tmp/" + filename
        else:
            filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_" + filename
        filename = directory + "/" + filename
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        return filename

    def show_tree_building_process(self):
        """
        Prints the progress of the tree building process in a readable format.
        """
        spaces = ""
        for i in range(self.node_depth):
            spaces += "|     "
        print(f"{spaces}{self.node_depth}. {self.node_value}: {list(self.labels_encodes.keys())[self.split_attribute]}")





def main():
    df = pd.read_csv("Uno/games_data/MergedCSV/20240728_2356_uno_game_693MB_testing.csv")
    df = prepare_data_for_learning(df)
    df, label_encoders = encode_data(df)
    print("Data loaded...")
    X_data = df.iloc[:, :-1].to_numpy()
    Y_data = df.iloc[:, -1].to_numpy()
    start = time.time()
    tree = C4_5Tree(X_data=X_data, Y_data=Y_data, remaining_data_indices=df.index.to_numpy(),
                    labels_encodes=label_encoders)
    tree.build_tree(max_depth=3, min_values_per_leaf=100, min_gain_ratio=0.04)
    tree.save_tree("C4_5Tree_tree.pkl")
    print(f"Tree successfully built in {time.time() - start} seconds.")

if __name__ == "__main__":
    main()





























