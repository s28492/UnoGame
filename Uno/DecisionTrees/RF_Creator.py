#!/usr/bin/env python3
import argparse
from datetime import time

from .BuildTree import buildTree
from ..games_data.dataHandler import prepareDataForTree
import pandas as pd
import os
import time

def createFolderForRF(num_of_trees = 10, depth=2, sample_proportion=0.63, duplicate_sample_elements=True, number_of_att_considered=2):
    folder_path=f'Uno/DecisionTrees/RandomForests/RandomForest_n{num_of_trees}_d{depth}_sp{sample_proportion}_dse{duplicate_sample_elements}_noac{number_of_att_considered}'
    new_path = folder_path
    i = 1
    while(os.path.exists(new_path) and os.listdir((new_path))!=[]):
        new_path = f"{folder_path}({i})"
        i += 1
    if (os.path.exists(new_path) and os.listdir((new_path))==[]) or not os.path.exists(new_path):
        os.mkdir(new_path)
    return new_path


def createTrees(num_of_trees = 10, depth=4, sample_proportion=0.63, duplicate_sample_elements=True, filepath='/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240802_0846_uno_game.csv', number_of_att_considered=2):
    df: pd.DataFrame = prepareDataForTree(pd.read_csv(filepath))
    folder_name = createFolderForRF(num_of_trees=num_of_trees, depth=depth, sample_proportion=sample_proportion, duplicate_sample_elements=duplicate_sample_elements, number_of_att_considered=number_of_att_considered)
    start_time = time.time()
    for i in range(1, num_of_trees+1):
        sample_df = df.sample(frac=sample_proportion, replace=duplicate_sample_elements)
        tree = buildTree(depth=depth, data_frame=sample_df, save_tree=False, forest=True, numebr_of_att_considered=2)
        tree.save_tree(f"tree{i}", is_temporary=False, directory=folder_name)
        del sample_df

    print(f"All {num_of_trees} trees created in {time.time() - start_time} seconds")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=4, help='depth of tree')
    parser.add_argument('--filepath', type=str,
                        default='/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240802_0846_uno_game.csv',
                        help='link for csv file to train the tree on')
    args = parser.parse_args()
    createTrees(depth=args.depth, filepath=args.filepath)