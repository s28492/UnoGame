import Player
from Card import StopCard


class AIPlayer (Player):
    def __init__(self, name: str):
        """Initializes AIPlayer"""
        super().__init__(name)
