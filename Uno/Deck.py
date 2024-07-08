import itertools

from Card import Card, ReverseCard, StopCard, Plus2Card, Plus4Card, ColorCard
import random


class Deck:
    colors = ["Red", "Green", "Blue", "Yellow"]
    values = [f"{i}" for i in range(10)]
    def __init__(self):
        self.deck = self.create_deck()
        self.shuffle_deck()

    def create_deck(self) -> list:
        """Creates deck of cards and returns it"""
        deck = []
        for card in itertools.product(self.values, self.colors):  # 19 for each color
            deck.append(Card(card[0], card[1]))
            if card[0] != 0:
                deck.append(Card(card[0], card[1]))

        for card in itertools.product(["Reverse"], self.colors):  # 2 for each color
            deck.append(ReverseCard(card[0], card[1]))
            deck.append(ReverseCard(card[0], card[1]))

        for card in itertools.product(["Stop"], self.colors):  # 2 for each color
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))

        for card in itertools.product(["+2"], self.colors):  # 2 for each color
            deck.append(Plus2Card(card[0], card[1]))
            deck.append(Plus2Card(card[0], card[1]))

        for card in itertools.product(["+4"], self.colors):  # 1 for each color
            deck.append(Plus4Card(card[0], card[1]))

        for i in range(4):  # 1 for each color
            deck.append(ColorCard("All", "Colors"))
        return deck

    def get_deck_len(self):
        return len(self.deck)

    def shuffle_deck(self) -> None:
        """shuffles the deck"""
        random.shuffle(self.deck)

    def draw_card(self):
        if not self.deck:
            return None
        return self.deck.pop()

    def cards_to_deck(self, hand):
        for card in hand:
            self.deck.append(card)

    def reshuffle_discard_pile(self, discard_pile):
        if len(discard_pile) >= 1:
            print("HHHHHHHHHHHHHHHHHHHHHHERE")
            self.deck.append(discard_pile)
            self.shuffle_deck()
        else:
            print("No cards left to reshuffle!")

    def deck_length(self):
        return len(self.deck)