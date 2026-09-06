import numpy as np
import pandas as pd
import random
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.game.Card import Card, Plus4Card, ColorCard, DrawCard, Plus2Card, StopCard
from Uno.AIPlayers.MonteCarloTreeSearch.Simulation import Simulation
from Uno.AIPlayers.MonteCarloTreeSearch.Node import Node



class MCTSBot(BaseAIBot):
    '''Flat Determinized Monte Carlo Search'''
    def __init__(self, name, num_of_simulations: int = 500, c_param=2):
        super().__init__(f"{name} sim:{num_of_simulations}_c:{c_param}")
        self.num_of_simulations = num_of_simulations
        self.c_param = c_param
        self.wins = 0
        self.simulations = 0
        self.root:Node = None
        self.hand = []

    def get_config(self):
        return {
            "type": "MCTSBot",
            "num_simulations": self.num_of_simulations,
            "c_param": self.c_param
        }


    def first_card_taken_actions(self, first_card_taken: Card):
        actions = []
        if isinstance(first_card_taken, Plus4Card):
            actions += self.create_color_cards(plus_card=True)
        elif isinstance(first_card_taken, ColorCard):
            actions += self.create_color_cards(plus_card=False)
        else:
            actions.append(first_card_taken)
        if len(actions) == 0:
            actions.append(DrawCard())
        return actions

    def taking_actions(self):
        actions = []
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
        if len(actions) == 0:
            actions.append(DrawCard())
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
        if len(actions) == 0:
            actions.append(DrawCard())
        return actions

    def all_valid_actions(self, first_card_taken=None):
        is_first_card_taken = first_card_taken is not None
        have_to_take = self.cards_to_take != 0
        have_to_stop = self.turns_to_stop != 0

        # Card was already taken from deck but can be put instantly
        if is_first_card_taken:
            return self.first_card_taken_actions(first_card_taken)

        # Collects valid actions if you need to take or to beat it
        if have_to_take:
            return  self.taking_actions()

        # Shows actions if bot has to stop or beat with stop card
        if have_to_stop:
            return self.stop_actions()

        return self.normal_actions()

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
        self.simulations += 1
        self.wins += result

        return result


    def backpropagation(self, node, result):
        if node is not None:
            node.set_wins(node.get_wins() + result)
            node.set_visits(node.get_visits() + 1)
            self.backpropagation(node.get_parent(), result)

    def move(self, first_card_taken=None, game=None):
        current_state = game.get_game_state()
        valid_actions = self.all_valid_actions(first_card_taken)
        if len(valid_actions) == 1:
            return valid_actions[0]

        self.root = Node(state=current_state)
        self.root.add_children(valid_actions)

        for _ in range(self.num_of_simulations):
            node = self.selection()
            result = self.simulation(game=game, action=node.get_action())
            self.backpropagation(node, result)
            self.root.calculate_children_ucb(self.c_param)
        if self.root.sum_children_wins() != self.root.get_wins():
            raise Exception(f"Number of visits and wins don't match. Visits: {self.root.get_visits()} Wins: {self.root.sum_children_wins()}")
        return self.root.get_highest_visits_child().get_action()


