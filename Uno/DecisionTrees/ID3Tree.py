import numpy as np
import pandas as pd
import time
import pickle
from datetime import datetime
from multiprocessing import Pool, cpu_count

#from graphviz import Digraph


class ID3Tree:
    def __init__(self, dataset: pd.DataFrame, attributes_names, target_attribute: pd.Series
                 , indices_list=None, parent=None, value_of_attribute_splitting=None):
        self.dataset = dataset
        self.attributes_names = attributes_names
        self.target_attribute = target_attribute
        self.parent = parent
        self.children = []
        self.indices_list = indices_list
        if indices_list is None:
            self.indices_list = self.dataset.index.tolist()
        self.splitting_attribute = None
        self.label = None
        self.is_leaf = False
        self.value_of_attribute_splitting = value_of_attribute_splitting  #Value of an attribute that this node was splitted on
        self.leaf_data = None
    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def get_attributes(self):
        return self.attributes_names

    def get_indices(self):
        return self.indices_list

    def calculate_entropy(self, indices_list: list = None):
        '''Calculate the entropy of the tree'''
        if indices_list is None:  # if indices weren't given,
            indices_list = self.indices_list  #then we operate on class initial dataset indices
        entropy = 0
        counted_target_values = self.target_attribute.iloc[indices_list].value_counts()

        for i in range(counted_target_values.shape[0]):
            p_i = counted_target_values.iloc[i] / counted_target_values.sum()
            entropy -= p_i * np.log2(p_i)

        return entropy

    def calculate_split_entropy(self, indices_list: list, column: str):
        split_information = 0
        counted_target_values = self.dataset.loc[indices_list, column].value_counts()
        total_count = counted_target_values.sum()  # This is the same as len(indices_list)

        for count in counted_target_values:
            values_proportion = count / total_count
            split_information -= values_proportion * np.log2(values_proportion)
        return split_information

    def split_data_by_column(self, column):
        '''Create a split and return a list of lists of indices'''
        datasets = []
        for value in self.dataset.loc[self.indices_list, column].unique():  # takes all unique elements in column
            subset_indices = self.dataset.loc[(self.dataset[column] == value)
                                              & self.dataset.index.isin(self.indices_list)].index
            datasets.append(subset_indices)
        return [column, datasets]

    def find_best_attribute_to_split(self):
        current_entropy = self.calculate_entropy()
        best_information_gain = -float('inf')
        best_datasets_with_column = None
        for attribute in self.attributes_names:
            datasets = self.split_data_by_column(attribute)  #list of lists of indices and spliting column

            child_average_weighted_entropy = 0

            for child in datasets[1]:  # child is a list of indices
                child_average_weighted_entropy += self.calculate_entropy(child) * (
                        len(child) / len(self.indices_list))

            split_information = self.calculate_split_entropy(self.indices_list, attribute)
            if split_information == 0:
                continue

            gain_ratio = (current_entropy - child_average_weighted_entropy) / split_information
            if best_information_gain < gain_ratio:
                best_information_gain = gain_ratio
                best_datasets_with_column = datasets
        return [best_information_gain, best_datasets_with_column]

    def most_common_label(self):
        return self.target_attribute.iloc[self.indices_list].mode()[0]

    def labels_in_leaf(self):
        return self.target_attribute.iloc[self.indices_list]

    def build_tree(self, max_depth: int, min_values_in_leaf: int, min_gain_ratio: float, depth: int = 0):
        is_max_depth_reached = max_depth == 0
        is_subset_too_small = len(self.indices_list) < min_values_in_leaf
        attributes_left = len(self.attributes_names) > 1
        indexes_left = len(self.indices_list) > 1
        is_data_homogeneous = self.target_attribute.iloc[self.indices_list].value_counts().iloc[0] == \
                              self.target_attribute.iloc[self.indices_list].shape[0]

        if (is_data_homogeneous or is_max_depth_reached
                or is_subset_too_small or not (attributes_left and indexes_left)):
            self.is_leaf = True
            self.leaf_data = self.labels_in_leaf()
            self.label = self.most_common_label()
            return

        best_gain_ratio, best_attribute_and_datasets = self.find_best_attribute_to_split()
        if best_attribute_and_datasets is None or best_gain_ratio < min_gain_ratio:
            self.is_leaf = True
            self.leaf_data = self.labels_in_leaf()
            self.label = self.most_common_label()
            return

        self.splitting_attribute = best_attribute_and_datasets[0]

        splitted_indexes_list = best_attribute_and_datasets[1]
        spaces = ""
        for i in range(depth):
            spaces += "     "
        print(f"{spaces}{depth}. {self.value_of_attribute_splitting}: {self.splitting_attribute}")

        if depth == 0:
            # Use multiprocessing only at the first level
            with Pool(processes=cpu_count()) as pool:
                results = pool.starmap(self.create_and_build_subtree,
                                       [(subset_indices, max_depth, min_values_in_leaf, min_gain_ratio, depth + 1)
                                        for subset_indices in splitted_indexes_list if len(subset_indices) > 0])
                self.children.extend(results)
        else:
            for subset_indices in splitted_indexes_list:
                if len(subset_indices) == 0:
                    continue
                new_attributes_names = [attr for attr in self.attributes_names if attr != self.splitting_attribute]
                new_node = ID3Tree(self.dataset, new_attributes_names, self.target_attribute,
                                   indices_list=subset_indices, parent=self,
                                   value_of_attribute_splitting=self.dataset.loc[
                                       subset_indices[0], self.splitting_attribute])
                new_node.build_tree(max_depth - 1, min_values_in_leaf, min_gain_ratio, depth + 1)
                self.children.append(new_node)

    def create_and_build_subtree(self, subset_indices, max_depth, min_values_in_leaf, min_gain_ratio, depth):
        new_attributes_names = [attr for attr in self.attributes_names if attr != self.splitting_attribute]
        new_node = ID3Tree(self.dataset, new_attributes_names, self.target_attribute,
                           indices_list=subset_indices, parent=self,
                           value_of_attribute_splitting=self.dataset.loc[subset_indices[0], self.splitting_attribute])
        new_node.build_tree(max_depth - 1, min_values_in_leaf, min_gain_ratio, depth)
        return new_node

    def predict(self, data_to_predict: pd.DataFrame):
        if self.is_leaf:
            return self.leaf_data
        for child in self.children:
            if child.value_of_attribute_splitting == data_to_predict[self.splitting_attribute]:
                return child.predict(data_to_predict)
        print("None valid...")

    def show_tree(self, depth=0):
        indent = "    " * depth
        if self.is_leaf:
            print(f"{indent}{depth}. Leaf: {self.label}")
        else:
            print(f"{indent}{depth}. Attribute: {self.splitting_attribute}")
            for child in self.children:
                child.show_tree(depth + 1)

    def save_tree(self, filename):
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_"+filename
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


def load_tree(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

def main(file_name: str = '/media/perceptron/xD/Projekty/Python/UnoGame/Uno/games_data/20240714_1857_uno_game.csv'):
    df = pd.read_csv("/media/perceptron/xD/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240715_0840_merged.csv")
    start = time.time()
    df = df.loc[df["did_win"] == True]
    del df["did_win"]
    del df["game_id"]
    df.reset_index(drop=True, inplace=True)
    print(df)
    print(df.shape)
    id_tree = ID3Tree(df.iloc[:], df.columns.tolist()[:-1], df.iloc[:, -1])
    id_tree.build_tree(max_depth=4, min_values_in_leaf=300, min_gain_ratio=0.07)
    print(f"Build successfully completed in {time.time() - start} seconds")

    # Zapisz drzewo do pliku
    id_tree.save_tree('id_tree.pkl')

    predicted_value = id_tree.predict(df.iloc[-1])
    print(f"FINAL OUTCOME: {predicted_value} --> {df.iloc[-1, -1]}")
    # id_tree = load_tree("20240715_0322_id_tree.pkl")
    # print("Tree loaded")
    # id_tree.show_tree()

if __name__ == '__main__':
    main()
