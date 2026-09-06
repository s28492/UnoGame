#!/usr/bin/env python3
import argparse
import time
import pandas as pd
from ..games_data.dataHandler import prepare_data_for_learning

from Uno.DecisionTrees.ID3Tree import ID3Tree, encode_data
from Uno.DecisionTrees.RandomForest import RandomForest, encode_data


from Uno.ReportingUtils import ReportGenerator

def buildTree(depth: int,
         file_path: str = '/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240715_0651_merged.csv', data_frame=None, save_tree=True, forest=False, numebr_of_att_considered=None, notes=""):
    if data_frame is None:
        data_frame = pd.read_csv(file_path)
    start = time.time()
    data_frame = prepare_data_for_learning(data_frame)
    encoded_df, labels = encode_data(data_frame)
    
    config = {
        "depth": depth,
        "min_values_in_leaf": 2000,
        "min_gain_ratio": 0.07,
        "dataset_path": file_path,
        "is_forest": forest
    }

    if forest:
        id_tree = ID3Tree(encoded_df.iloc[:, :-1], encoded_df.columns.tolist()[:-1], encoded_df.iloc[:, -1].to_frame(),
                          attribute_encoders=labels)
        id_tree.build_tree(max_depth=depth, min_values_in_leaf=2000, min_gain_ratio=0.07)
    else:
        id_tree = RandomForest(encoded_df.iloc[:, :-1], encoded_df.columns.tolist()[:-1], encoded_df.iloc[:, -1].to_frame(),
                           label_encoders=labels, number_of_attributes_considered=numebr_of_att_considered)
        id_tree.build_tree(max_depth=depth, min_values_in_leaf=2000, min_gain_ratio=0.07)

    print(f"Build successfully completed in {time.time() - start} seconds")
    
    if save_tree:
        tree_name = 'id_tree.pkl'
        id_tree.save_tree(tree_name)
        
        # Generator Report
        reporter = ReportGenerator()
        reporter.save_training_report(
            model_name=tree_name,
            config=config,
            notes=notes
        )
        
    return id_tree

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=4, help='depth of tree')
    parser.add_argument('--filepath', type=str, default='/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240802_0846_uno_game.csv', help='link for csv file to train the tree on')
    args = parser.parse_args()
    buildTree(args.depth, args.filepath)