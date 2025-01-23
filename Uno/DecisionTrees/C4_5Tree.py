import argparse

import datetime
import pickle
import time
import os
from Uno.games_data.dataHandler import *


class C4_5Tree:

    def __init__(
            self, X_data: np.array, Y_data: np.array, remaining_data_indices: np.array = None,
            remaining_column_indices: np.array = None, labels_encodes: dict = None, parent: 'C4_5Tree' = None,
            node_depth: int = 0, is_leaf: bool = False, node_value: str = None, split_attribute: int = None,
            column_names: list =None
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
        self.column_names = column_names
        self.prediction_data = None
        self.children_map = None
        self.deleted_data = False

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

            # If split_information == 0 then to avoid division by 0 set information gain as 0
            if split_information == 0:
                gain_ratio = 0
            else:
                gain_ratio = information_gain / split_information

            gain_ratios.append(gain_ratio)
            all_split_values.append(split_values)
            all_split_indexes.append(split_indexes)

        # Convert information gains to numpy array for efficient operations
        gain_ratios = np.array(gain_ratios)

        # Find the best column
        best_column_idx = np.argmax(gain_ratios)
        # Adjust best index to reference "remaining_column_indexes" not "information_gains"
        best_column_index = self.remaining_column_indices[best_column_idx]
        best_split_values = np.array(all_split_values[best_column_idx])
        best_split_indexes = all_split_indexes[best_column_idx]

        max_gain_ratio = gain_ratios[best_column_idx]
        return best_column_index, max_gain_ratio, best_split_values, best_split_indexes




    def build_tree(self, max_depth: int, min_values_per_leaf: int, min_gain_ratio: float, show_building_peocess:bool=True) -> 'C4_5Tree':
        # Calculating the best split based on gain ratio
        self.__assign_prediction_data()
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
        if show_building_peocess:
            self.__show_tree_building_process()

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
                new_node.build_tree(max_depth, min_values_per_leaf, min_gain_ratio, show_building_peocess=show_building_peocess)
        if len(self.children) == 0:
            self.is_leaf = True
        return self



    def predict(self, data_to_predict: pd.DataFrame):
        encoded_data = encode_data_with_label(data_to_predict, self.labels_encodes)

        if self.is_leaf or self.children_map is None:
            return self.prediction_data


        child = self.children_map.get(encoded_data.iloc[0, self.split_attribute])
        if child:
            return child.predict(data_to_predict)
        return self.prediction_data

    def __assign_prediction_data(self):
        self.prediction_data = pd.Series(data=self.Y_data[self.remaining_data_indices]).replace(
            self.labels_encodes["card_played"].keys(), self.labels_encodes["card_played"].values()).value_counts(sort=True)


    def sort_children(self):
        self.children.sort(key=lambda x: x.node_value, reverse=False)
        for child in self.children:
            child.sort_children()

    def create_children_map(self):
        self.children_map = {child.node_value: child for child in self.children}

        for child in self.children:
            child.create_children_map()

    def drop_data(self):
        self.X_data = None
        self.Y_data = None
        self.remaining_data_indices = None
        self.remaining_column_indices = None
        self.node_depth = None
        self.deleted_data = True
        for child in self.children:
            child.drop_data()

    def save_tree(self, filename, is_temporary=False, directory="Uno/DecisionTrees/Models"):
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

    def __show_tree_building_process(self):
        """
        Prints the progress of the tree building process in a readable format.
        """
        spaces = ""
        for i in range(self.node_depth):
            spaces += "|     "
        print(f"{spaces}{self.node_depth}. {self.node_value}: {list(self.labels_encodes.keys())[self.split_attribute]} -> len: {self.remaining_data_indices.shape[0]}")

    def print_tree(self):
        str = ""
        for i in range(0, self.node_depth):
            str += f"\t"

        if self.parent == None:
            print(f"{str}{self.node_depth}. {self.node_value}")
        else:
            print(f"{str}{self.node_depth}. p_s={self.parent.split_attribute} -> n_v={self.node_value}")

        for child in self.children:
            child.print_tree()

def load_tree(filename):
    """
    Loads a serialized C4.5 decision tree from a file.

    Parameters:
        filename (str): The path to the file containing the serialized tree.

    Returns:
        C4.5Tree: The deserialized ID3 decision tree instance.
    """
    abs_path = os.path.abspath(filename)
    with open(abs_path, 'rb') as f:
        return pickle.load(f)



def main(file_path: str, depth: int=8):
    df = pd.read_csv(file_path)
    df = prepare_data_for_learning(df)
    print(df.head())
    # new_df = pd.DataFrame(columns=df.columns)
    # print(new_df["card_played"].value_counts())
    # print(f"Data loaded...: \n {df["card_played"].value_counts()}")
    df, label_encoders = encode_data(df)
    X_data = df.iloc[:, :-1].to_numpy()
    Y_data = df.iloc[:, -1].to_numpy()
    start = time.time()
    tree = C4_5Tree(X_data=X_data, Y_data=Y_data, remaining_data_indices=df.index.to_numpy(),
                    labels_encodes=label_encoders, column_names=df.columns.to_list()[:-1])
    max_depth = depth
    min_values_in_leaf = 200
    min_gain_ratio = 0.03
    tree.build_tree(max_depth=max_depth, min_values_per_leaf=min_values_in_leaf, min_gain_ratio=min_gain_ratio)
    print(f"Tree successfully built in {time.time() - start} seconds.")
    tree.save_tree(f"d{max_depth}_mvl{min_values_in_leaf}_gr{min_gain_ratio}.pkl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=3, help='depth of tree')
    parser.add_argument('--filepath', type=str,
                        default='Uno/games_data/MergedCSV/20240728_2356_uno_game_693MB_testing.csv',
                        help='link for csv file to train the tree on')
    args = parser.parse_args()
    main(file_path=args.filepath, depth=args.depth)






























