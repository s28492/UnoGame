from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.game.Card import Card, Plus4Card, ColorCard, DrawCard, Plus2Card, StopCard
from Uno.AIPlayers.MonteCarloTreeSearch.Simulation import Simulation
from Uno.AIPlayers.MonteCarloTreeSearch.Node import Node
from Uno.game.GameState import GameState


import numpy as np
import pandas as pd
import random
from numpy.ma.extras import average


class MCTSBot(BaseAIBot):
    def __init__(self, name, num_of_simulations: int = 15, c_param=2):
        super().__init__(f"{name} sim:{num_of_simulations}_c:{c_param}")
        self.num_of_simulations = num_of_simulations
        self.c_param = c_param
        self.wins = 0
        self.simulations = 0
        self.root:Node = None


    def first_card_taken_actions(self, first_card_taken: Card):
        actions = []
        actions.append(DrawCard())
        if isinstance(first_card_taken, Plus4Card):
            actions += self.create_color_cards(plus_card=True)
        elif isinstance(first_card_taken, ColorCard):
            actions += self.create_color_cards(plus_card=False)
        else:
            actions.append(first_card_taken)
        return actions

    def taking_actions(self):
        actions = []
        actions.append(DrawCard())
        plus_4_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
        # Prevents duplicating of actions so the algorithm won't waste resources
        if len(plus_4_cards) != 0:
            actions += self.create_color_cards(plus_card=True)

        if not isinstance(self.card_on_top, Plus4Card):
            # Prevents duplicating of actions so the algorithm won't waste resources
            cards = self.collect_valid_cards_of_given_instance(Plus2Card)
            sorted(cards, key=lambda card: card.color)
            colors = []
            for card in cards:
                if card.color not in colors:
                    colors.append(card.color)
                    actions.append(card)
        return actions


    def stop_actions(self):
        actions = []
        actions.append(StopCard("Stop", "Stop"))
        cards = self.collect_valid_cards_of_given_instance(StopCard)
        colors = []
        for card in cards:
            if card.color not in colors:
                colors.append(card.color)
                actions.append(card)
        return actions

    def normal_actions(self):
        actions = []
        actions.append(DrawCard())
        duplicate_cards = []
        for card in self.hand:
            if card.match(self.card_on_top) and card not in duplicate_cards:
                if isinstance(card, Plus4Card):
                    actions += self.create_color_cards(plus_card=True)
                elif isinstance(card, ColorCard):
                    actions += self.create_color_cards(plus_card=False)
                else:
                    actions.append(card)
                duplicate_cards.append(card)
        return actions

    def all_valid_actions(self, first_card_taken=None):
        is_first_card_taken = first_card_taken is not None
        have_to_take = self.cards_to_take != 0
        have_to_stop = self.turns_to_stop != 0

        # Card was already taken from deck but can be put instantly
        if is_first_card_taken:
            # print("First card taken...")
            return self.first_card_taken_actions(first_card_taken)

        # Collects valid actions if you need to take or to beat it
        if have_to_take:
            # print("Taking card...")
            return  self.taking_actions()

        # Shows actions if bot has to stop or beat with stop card
        if have_to_stop:
            # print("Stopping card...")
            return self.stop_actions()

        # print("Normal actions...")
        return self.normal_actions()

    # UCT =


    def selection(self):
        return self.root.get_highest_ucb_child()


    def expand(self, node):
        action = node.get_action()
        new_state = node.state.apply_action(action, node.state.current_player)
        child_node = node.add_child(action, new_state)
        return child_node

    def simulation(self, game, action):
        simulation = Simulation(game, self.hand, action)
        simulation.initialize_game()
        result = simulation.play()
        # print(f"Simulation for {action.rich_str()}: {result}")
        # print("\n\n=========================================================\n\n")
        self.simulations += 1
        self.wins += result

        return result


    def backpropagation(self, node, result):
        # print(result)
        if node is not None:
            node.set_wins(node.get_wins() + result)
            node.set_visits(node.get_visits() + 1)
            self.backpropagation(node.parent, result)


    def create_new_states(self, actions):
        for action in actions:
            new_state = self.root.state.apply_action(action, self.root.state.current_player)

    def print_valid_actions(self):
        valid_actions = self.all_valid_actions()
        valid_act_str = ""
        for action in valid_actions:
            valid_act_str += f"{action} | "
        print(">>> Valid actions: ", valid_act_str)

    def move(self, first_card_taken=None, game=None):
        # print("=============")
        current_state = game.get_game_state()
        valid_actions = self.all_valid_actions(first_card_taken)
        if len(valid_actions) == 1:
            return valid_actions[0]
        # self.print_valid_actions()

        self.root = Node(state=current_state)
        self.root.add_children(valid_actions)

        simulation_iterator = 1
        for _ in range(self.num_of_simulations):
            node = self.selection()
            # print(f"children ucb: {self.root.get_children_ucb()}")
            # print(f"{simulation_iterator}) {node.get_action()} -> {node.get_ucb()}")
            # print(f"Node: {node.get_action()} -> {node.get_ucb()}")
            result = self.simulation(game=game, action=node.get_action())
            self.backpropagation(node, result)
            self.root.calculate_children_ucb(self.c_param)
            simulation_iterator += 1
            # print("\n")
        # if isinstance(self.root.get_highest_ucb_child().get_action(), DrawCard) and len(valid_actions) > 1:
        #     print("Unreasonable draw...")

        # print("Card on top: ", self.card_on_top)
        # print(self.root.get_children_ucb())
        # print("Card played: ", self.root.get_highest_ucb_child().get_action(), "\n")

        # print("Winrate: ", self.wins / self.simulations)
        # self.wins = 0
        # self.simulations = 0


        # print(self.root.get_children_winrate(), "\n\n")

        # print("Action taken: ", self.root.get_highest_ucb_child().get_action())
        if self.root.sum_children_wins() != self.root.get_wins():
            raise Exception(f"Number of visits and wins don't match. Visits: {self.root.get_visits()} Wins: {self.root.sum_children_wins()}")
        return self.root.get_highest_ucb_child().get_action()


