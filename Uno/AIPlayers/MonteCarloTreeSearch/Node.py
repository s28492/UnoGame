import numpy as np
import math
class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.__parent = parent
        self.__children = []
        self.__visits = 0
        self.__wins = 0
        self.__action = action
        self.__ucb = float('inf')
        self.__is_leaf = True

    def get_state(self):
        return self.state

    def get_visits(self):
        return self.__visits

    def set_visits(self, visits):
        self.__visits = visits

    def get_wins(self):
        return self.__wins

    def set_wins(self, wins):
        self.__wins = wins

    def get_winrate(self):
        if self.__visits == 0:
            return 0
        return self.__wins / self.__visits

    def get_children(self):
        return self.__children

    def get_highest_ucb_child(self):
        max_ucb = -float('inf')
        max_child = None
        for child in self.__children:
            if child.get_ucb() == 'inf':
                return child
            elif child.get_ucb() > max_ucb:
                max_ucb = child.get_ucb()
                max_child = child
        return max_child

    def get_children_ucb(self):
        action_ucb = {}
        for child in self.__children:
            action_ucb[f"{child.get_action()}"] = child.__ucb
        return action_ucb

    def get_highest_visits_child(self):
        max_visits = -float('inf')
        max_child = None
        for child in self.__children:
            if child.__visits > max_visits:
                max_visits = child.__visits
                max_child = child
        return max_child

    def get_children_visits(self):
        action_visits = {}
        for child in self.__children:
            action_visits[f"{child.get_action()}"] = child.get_visits()
        return action_visits

    def sum_children_wins(self):
        sum = 0
        for child in self.__children:
            sum += child.__wins
        return sum

    def get_children_winrate(self):
        action_winrate = {}
        for child in self.__children:
            action_winrate[f"{child.get_action()}"] = child.get_winrate()
        return action_winrate

    def get_ucb(self):
        return self.__ucb

    def get_action(self):
        return self.__action

    def get_parent(self):
        return self.__parent

    def calculate_ucb(self, c_param=2):
        if self.__parent is not None:
            if self.__visits == 0:
                self.__ucb = float('inf')
            # print(f"Setting UCB for {self.action}: s_w {self.wins}, s_v {self.visits} , p_v {np.log(self.parent.visits)} , c_p {c_param} , ucb={self.ucb}")
            else:
                self.__ucb = (self.__wins / self.__visits) + c_param * math.sqrt(
                (math.log(self.__parent.__visits) / self.__visits))
            return self.__ucb

    def calculate_children_ucb(self, c_param=2):
        if self.__children is not None:
            for child in self.__children:
                child.calculate_ucb(c_param)
                child.calculate_children_ucb(c_param)


    def add_child(self, action):
        child_node = Node(state=self.state, parent=self, action=action)
        self.__children.append(child_node)
        return child_node

    def add_children(self, actions):
        for action in actions:
            self.add_child(action)