class Node:
    def __init__(self, prior, to_play):
        self.prior = prior
        self.to_play = to_play

        self.children = []
        self.visits = 0
        self.value_sum = 0
        self.state = None