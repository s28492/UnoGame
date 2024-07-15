import pandas as pd
from Uno.DecisionTrees.ID3Tree import ID3Tree, load_tree
from Uno.players.Bot import Bot
from Uno.game.Card import *
class ID3Bot(Bot):
    def __init__(self, name:str
                 , tree_file:str="/media/perceptron/xD/Projekty/Python/UnoGame/Uno/DecisionTrees/20240715_0322_id_tree.pkl"):
        super().__init__(name)
        self.current_data = pd.DataFrame()
        self.id_tree = load_tree(tree_file)

    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                if isinstance(card, ColorCard) and not isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        valid_cards_to_put.append(ColorCard(color, card.color))
                elif isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        valid_cards_to_put.append(Plus4Card(color, card.color))
        return valid_cards_to_put

    def valid_cards(self, card_taken = None) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        if card_taken is not None:
            return [card_taken, DrawCard()]

        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            valid_cards.append(StopCard("Stop", "Stop"))
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            valid_cards.append(DrawCard())
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus2Card) + self.collect_valid_cards_of_given_instance(Plus4Card)
            valid_cards.append(DrawCard())
            return valid_cards

        valid_cards = self.collect_valid_cards_of_given_instance(Card)
        valid_cards.append(DrawCard())

        return valid_cards

    def create_row(self, dict):
        row = pd.Dataframe.from_dict(dict, orient='index')
        self.current_data = pd.concat([self.current_data, row], axis=1, ignore_index=True)
        print(self.current_data)
    def create_dataframe(self):
        features = self.extract_features()

    def filter_cards_from_hand(self, node):
        cards_occurences_dict = {}
        for card in self.hand:
            if not isinstance(card, ColorCard):
                if card not in cards_occurences_dict:
                    cards_occurences_dict[card] = 1
                else:
                    cards_occurences_dict[card] += 1
            elif isinstance(card, Plus4Card):
                pass

    def card_in_current_node_amoount(self, cards, node):
        for card in cards:
            if isinstance(card, Plus4Card):
                pass

    def move(self, first_card_taken=None):
        valid_cards = self.valid_cards(card_taken=first_card_taken)
        node_values = self.id_tree.predict(self.current_data)
        print(node_values)


