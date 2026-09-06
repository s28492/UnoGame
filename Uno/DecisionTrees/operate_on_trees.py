from Uno.DecisionTrees.C4_5Tree import load_tree, C4_5Tree


#from graphviz import Digraph


def concatenate_tree():
    tree = load_tree('Uno/DecisionTrees/Models/20241227_1251_3GB_Dataset_with_child_map.pkl')
    tree.drop_data()
    tree.save_tree('LIGHT_20241227_1251_3GB_Dataset_with_child_map.pkl', directory="Uno/DecisionTrees/LightModels")



if __name__ == '__main__':
    concatenate_tree()
