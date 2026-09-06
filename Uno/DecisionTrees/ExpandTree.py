import argparse
from Uno.DecisionTrees.ID3Tree import ID3Tree, load_tree
import time

def main(depth:int, file_path: str):
    tree: ID3Tree = load_tree(file_path)
    print("Tree loaded succesfully")
    start = time.time()
    print(f"Nodes to expand: {len(tree.find_leafs_with_values_more_or_equal_than(number_of_elements_in_leaf=2_000))}")
    tree.expand_tree(depth, 2_000, 0.08)
    print(f"Tree expanded succesfully in {time.time() - start} seconds")
    tree.save_tree(f"expanded_tree_d{tree.get_distance_to_farthest_leaf()}.pkl")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=9, help='depth of tree')
    parser.add_argument('--filepath', type=str, default='/mnt/587A903A7A90173A/Projekty/Python/NewUnoGame/UnoGame/Uno/DecisionTrees/20240823_0253_expanded_tree_d9.pkl', help='link for csv file to train the tree on')
    args = parser.parse_args()
    main(args.depth, args.filepath)
