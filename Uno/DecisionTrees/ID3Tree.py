import argparse
from numba import jit, njit, vectorize
import numpy as np
import pandas as pd
import time
import pickle
from datetime import datetime
from multiprocessing import Pool, cpu_count
from sklearn.preprocessing import LabelEncoder
import os


class ID3Tree:
    def __init__(self, dataset: pd.DataFrame, attributes_names, target_attribute: pd.Series
                 , label_encoders=None, indices_list=None,
                 parent=None, value_of_attribute_splitting=None, node_depth: int = 0):
        self.label_encoders = label_encoders
        self.dataset = dataset
        self.attributes_names = attributes_names
        self.target_attribute = target_attribute
        self.parent = parent
        self.children: list[ID3Tree] = []
        if indices_list is not None:
            self.indices_list = indices_list
        else:
            self.indices_list = self.dataset.index.tolist()
        self.splitting_attribute = None
        self.label = None
        self.is_leaf = False
        self.value_of_attribute_splitting = value_of_attribute_splitting
        # self.leaf_data = None
        self.node_depth = node_depth

    def get_children(self):
        return self.children

    def get_splitting_attribute(self):
        return self.splitting_attribute

    def get_attributes(self):
        return self.attributes_names

    def get_indices(self):
        return self.indices_list

    def get_label_encoders(self):
        return self.label_encoders

    def encode_df(self):
        pass
    def decode_target_values(self):
        if self.label_encoders is not None and self.parent is None:
            self.target_attribute = decode_data(self.target_attribute, label_encoders= self.label_encoders)
        elif self.label_encoders is not None and self.parent is not None:
            self.target_attribute = self.parent.target_attribute
        for child in self.children:
            print("AAAAA")
            child.decode_target_values()
    def decode_values(self):
        if self.parent is not None:
            self.value_of_attribute_splitting = self.label_encoders[self.parent.get_splitting_attribute()][self.value_of_attribute_splitting]
        for child in self.children:
            child.decode_values()
    def decode_df(self):
        if self.label_encoders is not None:
            dataset = decode_data(pd.concat([self.dataset, self.target_attribute]), self.label_encoders)
            self.dataset = dataset[self.attributes_names]
            self.target_attribute = dataset.iloc[:, -1].to_frame()
        #self.decode_values()
    def get_entropy(self, indices_list: list = None):
        if indices_list is None:
            indices_list = self.indices_list
        counted_target_values = self.target_attribute.iloc[indices_list].value_counts().to_numpy()
        return calculate_entropy_numba(counted_target_values)

    def calculate_split_entropy(self, indices_list: list, column: str):
        counted_target_values = self.dataset.loc[indices_list, column].value_counts().to_numpy()
        return calculate_split_information(counted_target_values)

    def split_data_by_column(self, column):
        datasets = []
        for value in self.dataset.loc[self.indices_list, column].unique():
            subset_indices = self.dataset.loc[(self.dataset[column] == value)
                                              & self.dataset.index.isin(self.indices_list)].index
            datasets.append(subset_indices)
        return [column, datasets]

    def get_gain_ratio(self, attribute, current_entropy):
        datasets = self.split_data_by_column(attribute)
        child_counts = [self.target_attribute.iloc[subset_indices].value_counts().to_numpy() for subset_indices in
                        datasets[1]]
        gain_ratio = calculate_gain_ratio(child_counts, current_entropy, len(self.indices_list))
        return gain_ratio, datasets

    def find_best_attribute_to_split(self):
        current_entropy = self.get_entropy()
        best_information_gain = -float('inf')
        best_datasets_with_column = None
        num_of_processe = cpu_count() - 1 if cpu_count() > 1 else 1
        with Pool(processes=num_of_processe) as pool:
            results = pool.starmap(self.get_gain_ratio,
                                   [(attribute, current_entropy)
                                    for attribute in self.attributes_names])
            pool.close()
            pool.join()

        for gain_ratio, datasets in results:
            if gain_ratio is not None and best_information_gain < gain_ratio:
                best_information_gain = gain_ratio
                best_datasets_with_column = datasets
        return [best_information_gain, best_datasets_with_column]

    def is_tree_done(self, max_depth, min_values_in_leaf, min_gain_ratio):
        is_max_depth_reached = max_depth == 0
        is_subset_too_small = len(self.indices_list) < min_values_in_leaf
        attributes_left = len(self.attributes_names) > 1
        indexes_left = len(self.indices_list) > 1
        is_data_homogeneous = self.target_attribute.iloc[self.indices_list].value_counts().iloc[0] == \
                              self.target_attribute.iloc[self.indices_list].shape[0]

        if not (is_data_homogeneous or is_max_depth_reached or is_subset_too_small or not (
                attributes_left and indexes_left)):
            best_gain_ratio, best_attribute_and_datasets = self.find_best_attribute_to_split()
            if not best_attribute_and_datasets is None or best_gain_ratio < min_gain_ratio:
                return best_gain_ratio, best_attribute_and_datasets
        self.is_leaf = True
        self.label = self.most_common_label()
        return None, None

    def build_tree(self, max_depth: int, min_values_in_leaf: int, min_gain_ratio: float):
        best_gain_ratio, best_attribute_and_datasets = self.is_tree_done(max_depth, min_values_in_leaf, min_gain_ratio)
        if best_gain_ratio is None or best_attribute_and_datasets is None:
            return

        self.splitting_attribute = best_attribute_and_datasets[0]
        splitted_indexes_list = best_attribute_and_datasets[1]

        self.show_tree_building_process()

        for subset_indices in splitted_indexes_list:
            if len(subset_indices) == 0:
                continue
            new_attributes_names = [attr for attr in self.attributes_names if attr != self.splitting_attribute]
            new_node = ID3Tree(self.dataset, new_attributes_names, self.target_attribute,
                               label_encoders=self.label_encoders, indices_list=subset_indices, parent=self,
                               value_of_attribute_splitting=self.dataset.loc[
                                   subset_indices[0], self.splitting_attribute], node_depth=self.node_depth + 1)
            new_node.build_tree(max_depth - 1, min_values_in_leaf, min_gain_ratio)
            self.children.append(new_node)

    def show_tree_building_process(self):
        spaces = ""
        for i in range(self.node_depth):
            spaces += "     "
        print(f"{spaces}{self.node_depth}. {self.value_of_attribute_splitting}: {self.splitting_attribute}")

    def find_leafs(self, list_of_leafs=None):
        if list_of_leafs is None:
            list_of_leafs = []
        if self.is_leaf:
            list_of_leafs.append(self)
            return list_of_leafs
        for child in self.children:
            if child.is_leaf:
                list_of_leafs.append(child)
            else:
                child.find_leafs(list_of_leafs)
        return list_of_leafs

    def expand_tree(self, max_depth: int, min_values_in_leaf: int, min_gain_ratio: float):
        # 1. Wczytac wszystkie liscie (Done)
        # 2. Zapisac wszystkie poddrzewa korzenia
        # 3. Wczytywać każde poddrzewo pojedyńczo
        # 4. Rozbudowywać poddrzewo
        # 5. Zapisać poddrzewo jako rozbudowane
        # 6. Usunąć drzewo z ramu
        # 7. -> 3
        # 8. Po rozbudowaniu każdego korzenia (lub może również po komendzie użytkownika)
        # połączyć wszystkie rozbudowane do tej pory drzewa.
        # 9. Zapisać główne drzewo.
        self.dataset = encode_data_with_label(self.dataset, self.label_encoders)
        for i, child in enumerate(self.children):
            child.save_tree(f"tmp_node_{self.node_depth}_{i}.pkl", is_temporary=True)
        self.children = []
        folder = "tmp"

        for root, dirs, files in os.walk(folder):
            for i, file in enumerate(files):
                if file.startswith(f'tmp_node_{self.node_depth}'):
                    full_path = os.path.join(root, file)
                    print(f'Znaleziono plik: {full_path}')
                    tmp_tree: ID3Tree = load_tree(full_path)
                    leafs: list[ID3Tree] = tmp_tree.find_leafs()
                    print(f"Number of leafs: {len(leafs)}")
                    for leaf in leafs:
                        leaf.change_leaf_status()
                        leaf.build_tree(max_depth - leaf.node_depth, min_values_in_leaf, min_gain_ratio)
                    tmp_tree.save_tree(f"expanded_node_{i}.pkl", is_temporary=True)
                    remove_file(full_path)

        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.startswith('expanded'):
                    full_path = os.path.join(root, file)
                    print(f'Znaleziono plik: {full_path}')
                    tmp_tree: ID3Tree = load_tree(full_path)
                    self.children.append(tmp_tree)
                    remove_file(full_path)
        self.save_tree("id_tree.pkl")

    def get_distance_to_farthest_leaf(self, recurrent_call: bool = False):
        if self.is_leaf and recurrent_call:
            return 1
        elif self.is_leaf:
            return 0
        depths_tab = []
        for child in self.children:
            depths_tab.append(child.get_distance_to_farthest_leaf(recurrent_call=True))
        return 1 + max(depths_tab)

    def most_common_label(self):
        return self.target_attribute.iloc[self.indices_list].mode()

    def change_leaf_status(self):
        self.is_leaf = False
        self.label = None

    def labels_in_node(self):
        return self.target_attribute.iloc[self.indices_list]

    def predict(self, data_to_predict: pd.DataFrame):
        if isinstance(data_to_predict, pd.Series):
            data_to_predict = data_to_predict.to_frame().T

        data_to_predict = pd.DataFrame([data_to_predict.values[0]], columns=data_to_predict.columns)

        if self.is_leaf:
            data = self.target_attribute.iloc[self.indices_list]
            return data

        final_value = data_to_predict[self.splitting_attribute].iloc[0]

        for child in self.children:
            if child.value_of_attribute_splitting == final_value:
                return child.predict(data_to_predict)

        data = self.target_attribute.iloc[self.indices_list]
        return data

    def show_tree(self, depth=0):
        indent = "    " * depth
        print(f"{indent}  {self.value_of_attribute_splitting}")
        if self.is_leaf:
            print(f"{indent}{depth}. Leaf: {self.label}")
        else:
            print(f"{indent}{depth}. Attribute: {self.splitting_attribute}")
            for child in self.children:
                child.show_tree(depth + 1)

    def save_tree(self, filename, is_temporary=False):
        if is_temporary:
            filename = "tmp/" + filename
        else:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_" + filename
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        return filename

    def create_leaf_map(self, path=None, list_of_paths=None):
        if list_of_paths is None:
            list_of_paths = []
        if path is None:
            path = []

        if self.is_leaf:
            list_of_paths.append(path + [self.value_of_attribute_splitting])
            return list_of_paths

        for child in self.children:
            if self.value_of_attribute_splitting is None:
                child.create_leaf_map(path, list_of_paths)
            else:
                new_path = path + [self.value_of_attribute_splitting]
                child.create_leaf_map(new_path, list_of_paths)

        return list_of_paths

    def go_to_given_node(self, path):
        if len(path) == 0:
            return self

        for child in self.children:
            if child.value_of_attribute_splitting == path[0]:
                return child.go_to_given_node(path[1:])
        print("path_doesnt_exist")


@njit(nogil=True)
def calculate_gain_ratio(counted_values, current_entropy, total_indices_count):
    child_average_weighted_entropy = 0
    for child_count in counted_values:
        child_entropy = calculate_entropy_numba(child_count)
        child_average_weighted_entropy += child_entropy * (np.sum(child_count) / total_indices_count)

    split_information = calculate_split_information(np.array([np.sum(child) for child in counted_values]),
                                                    total_indices_count)
    if split_information == 0:
        return -1

    gain_ratio = (current_entropy - child_average_weighted_entropy) / split_information
    return gain_ratio


@njit(nogil=True)
def calculate_entropy_numba(counted_values):
    entropy = 0
    total_count = counted_values.sum()
    for count in counted_values:
        if count > 0:
            p_i = count / total_count
            entropy -= p_i * np.log2(p_i)
    return entropy


@njit(nogil=True)
def calculate_split_information(counted_target_values, total_count) -> float:
    split_information = 0
    for count in counted_target_values:
        if count > 0:
            values_proportion = count / total_count
            split_information -= values_proportion * np.log2(values_proportion)
    return split_information


def load_tree(filename):
    abs_path = os.path.abspath(filename)
    with open(abs_path, 'rb') as f:
        return pickle.load(f)


def remove_file(file_path: str):
    try:
        os.remove(file_path)
        print("Plik został usunięty.")
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
    except PermissionError:
        print("Brak uprawnień do usunięcia pliku.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

#
# def encode_columns(df, columns=None):
#     label_encoders = {}
#     if isinstance(df, pd.Series):
#         df = df.to_frame()
#         columns = df.columns
#     for column in columns:
#         le = LabelEncoder()
#         encoded = le.fit_transform(df[column])
#         df[column] = encoded.astype(df[column].dtype)  # Ustawienie odpowiedniego typu danych
#         label_encoders[column] = le
#     return df, label_encoders
#
#
# def decode_columns(df, columns, label_encoders):
#     for column in columns:
#         le = label_encoders[column]
#         # Sprawdzenie typów danych przed dekodowaniem
#         if not np.issubdtype(df[column].dtype, np.integer):
#             print(df[column].iloc[0])
#             raise ValueError(f"Column '{column}' contains non-integer values: {df[column].dtype}")
#         # Dekodowanie kolumny
#         decoded = le.inverse_transform(df[column].values)
#         df[column] = decoded
#     if len(df.columns) == 1:
#         return df.iloc[:, 0]
#     return df
def encode_data(df: pd.DataFrame):
    label_encoders = {}
    for column in df.columns.to_list():
        df[column], label_encoders[column] = create_column_label(df[column])
    # print("\n\n")
    # print(df.head())
    # print("\n\n")
    # print("Tu")
    return df, label_encoders
def create_column_label(column:pd.Series):
    counted_values = column.value_counts()
    encoded_column = {}
    # print(f"Column {column.name}")
    for i in range(counted_values.shape[0]):
        encoded_column[i] = counted_values.index.to_list()[i]
        # print(column)
    distinct_values = column.nunique()
    # print(distinct_values)
    # print(column)
    if column.dtype == "bool":
        column = column.astype(np.bool)
    else:
        if distinct_values < 256:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint8)
        elif distinct_values < 65536:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint16)
        elif distinct_values < 4294967295:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint32)
        elif distinct_values < 4294967296:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint64)
    return column, encoded_column

def decode_data(df: pd.DataFrame, label_encoders):
    new_df = pd.DataFrame()
    for column in df.columns.to_list():
        new_df[column] = df[column].replace(label_encoders[column].keys(), label_encoders[column].values())

    return new_df

def encode_data_with_label(df: pd.DataFrame, label_encoders):
    for column in df.columns.to_list():

        df[column] = df[column].replace(label_encoders[column].values(), label_encoders[column].keys()).astype(np.int32)
    return df

def main(depth: int,
         file_path: str):

    df: pd.DataFrame = pd.read_csv(file_path)
    start = time.time()
    df: pd.DataFrame = df.loc[df["did_win"] == True]
    del df["did_win"]
    del df["game_id"]
    df.reset_index(drop=True, inplace=True)
    encoded_df, labels = encode_data(df)
    print(encoded_df.info())
    #df = pd.DataFrame()
    #print(encoded_df.info())
    # id_tree = ID3Tree(encoded_df.iloc[:, :-1], encoded_df.columns.tolist()[:-1], df.iloc[:, -1].to_frame())#, label_encoders=labels)
    id_tree = ID3Tree(encoded_df.iloc[:, :-1], encoded_df.columns.tolist()[:-1], encoded_df.iloc[:, -1].to_frame(), label_encoders=labels)
    id_tree.build_tree(max_depth=depth, min_values_in_leaf=2000, min_gain_ratio=0.08)
    # id_tree2.build_tree(max_depth=depth, min_values_in_leaf=2000, min_gain_ratio=0.08)
    id_tree.decode_df()
    #id_tree.save_tree('id_tree.pkl')
    id_tree.save_tree('id_tree2.pkl')
    #id_tree.decode_df()
    print(f"Build successfully completed in {time.time() - start} seconds")
    id_tree.show_tree()

    # id_tree: ID3Tree = load_tree("/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240810_0951_uno_game.csv")
    # predicted_values = id_tree.predict(id_tree.dataset.iloc[-1, :-1])
    # print(predicted_values)
    # #print(predicted_values.value_counts())
    # for index_card in predicted_values.value_counts().index.to_list():
    #     print(index_card[0])
    # id_tree2: ID3Tree = load_tree("/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/DecisionTrees/20240801_0059_id_tree2.pkl")
    # print("First tree:")
    # #id_tree.show_tree()
    # print(id_tree.predict(df.iloc[-1:, :-1]))
    # print("\n===============================\nSecond tree:")
    # print(id_tree2.predict(df.iloc[-1:, :-1]))
    # id_tree2.decode_df()
    # print("Dekoded")
    # #id_tree2.show_tree()
    # print(id_tree2.predict(df.iloc[-1:, :-1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=6, help='depth of tree')
    parser.add_argument('--filepath', type=str,
                        default='/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240810_0951_uno_game.csv',
                        help='link for csv file to train the tree on')
    args = parser.parse_args()
    main(args.depth, args.filepath)
