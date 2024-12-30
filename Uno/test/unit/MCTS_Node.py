import pytest
from Uno.game.Game import Game
from Uno.players.AgressiveBot import AgressiveBot

from Uno.AIPlayers.MonteCarloTreeSearch.Node import Node

def set_up_node():
    p1 = AgressiveBot("Agressive1")
    p2 = AgressiveBot("Agressive2")
    game = Game([p1, p2])
    node = Node(game.get_game_state())

    children = []
    for card in game.get_game_state().get_deck().get_deck()[0:2]:
        children.append(node.add_child(card))

    node.set_visits(2)
    node.set_wins(30)
    children[0].set_visits(1)
    children[0].set_wins(20)
    children[1].set_visits(1)
    children[1].set_wins(10)

    return node

def test_wins_assigment():
    node:Node = set_up_node()
    node_children = node.get_children()
    assert node.get_wins() == 30
    assert node.get_visits() == 2
    assert node_children[0].get_wins() == 20
    assert node_children[1].get_wins() == 10
    assert node_children[0].get_visits() == 1
    assert node_children[1].get_visits() == 1




def test_ucb_calculation():
    node:Node = set_up_node()
    #
    # for child in children:
    #     assert child.parent == node
    node.get_children()[0].calculate_ucb(c_param=2)
    first_child_ucb = node.get_children()[0].get_ucb()

    node.get_children()[1].calculate_ucb(c_param=2)
    second_child_ucb = node.get_children()[1].get_ucb()
    # assert True == True
    assert round(first_child_ucb, 2) == 21.67
    assert round(second_child_ucb, 2) == 11.67
