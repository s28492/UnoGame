import numpy as np
class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.action = action
        self.ucb = float('inf')
        self.is_leaf = True

    def get_visits(self):
        return self.visits

    def set_visits(self, visits):
        self.visits = visits

    def get_wins(self):
        return self.wins

    def set_wins(self, wins):
        self.wins = wins

    def get_winrate(self):
        if self.visits == 0:
            return 0
        return self.wins / self.visits

    def get_children(self):
        return self.children

    def get_highest_ucb_child(self):
        max_ucb = -float('inf')
        max_child = None
        for child in self.children:
            if child.get_ucb() == 'inf':
                return child
            elif child.get_ucb() > max_ucb:
                max_ucb = child.get_ucb()
                max_child = child
        return max_child

    def get_children_ucb(self):
        action_ucb = {}
        for child in self.children:
            action_ucb[f"{child.get_action()}"] = child.ucb
        return action_ucb

    def sum_children_wins(self):
        sum = 0
        for child in self.children:
            sum += child.wins
        return sum

    def get_children_winrate(self):
        action_winrate = {}
        for child in self.children:
            action_winrate[f"{child.get_action()}"] = child.get_winrate()
        return action_winrate

    def get_ucb(self):
        return self.ucb

    def get_action(self):
        return self.action

    def get_parent(self):
        return self.parent

    # def get_children_ucb(self):
    #     data = ""
    #     for child in self.children:
    #         data += f"{child.get_action()} ->{child.wins}/{child.visits} + {np.log(self.visits)}/{child.visits}-> {child.get_ucb()} | "
    #     return data

    def calculate_ucb(self, c_param=2):
        if self.parent is not None:
            if self.visits == 0:
                self.ucb = float('inf')
            # print(f"Setting UCB for {self.action}: s_w {self.wins}, s_v {self.visits} , p_v {np.log(self.parent.visits)} , c_p {c_param} , ucb={self.ucb}")
            else:
                self.ucb = (self.wins / self.visits) + c_param * np.sqrt(
                (np.log(self.parent.visits) / self.visits))
            return self.ucb


    # def is_fully_expanded(self):
    #     return len(self.untried_actions) == 0

    def calculate_children_ucb(self, c_param=2):
        if self.children is not None:
            for child in self.children:
                child.calculate_ucb(c_param)
                child.calculate_children_ucb(c_param)


    def add_child(self, action):
        child_node = Node(state=self.state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    def add_children(self, actions):
        for action in actions:
            self.add_child(action)