import itertools

from Uno.game.Card import Card, ReverseCard, StopCard, Plus2Card, Plus4Card, ColorCard
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
            if card[0] != "0":
                deck.append(Card(card[0], card[1]))

        for card in itertools.product(["Reverse"], self.colors):  # 2 for each color
            deck.append(ReverseCard(card[0], card[1]))
            deck.append(ReverseCard(card[0], card[1]))

        for card in itertools.product(["Stop"], self.colors):  # 2 for each color
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))

        for card in itertools.product(["+2"], self.colors):  # 2 for each color
            deck.append(Plus2Card(card[0], card[1]))
            deck.append(Plus2Card(card[0], card[1]))

        for card in itertools.product(["+4"], self.colors):  # 1 for each color
            deck.append(Plus4Card(card[0], card[1]))

        for i in range(4):                                   # 1 for each color
            deck.append(ColorCard("All", "Colors"))
        return deck

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck

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

    def reset_colored_cards(self, discard_pile):
        """Resets Colored cards being moved to the deck from pile"""
        for card in discard_pile:
            if isinstance(card, ColorCard):
                card.color = "Colors"
        return discard_pile

    def reshuffle_discard_pile(self, discard_pile):
        discard_pile = self.reset_colored_cards(discard_pile)
        self.deck += discard_pile
        self.shuffle_deck()


    def deck_length(self):
        return len(self.deck)

    def remove_card_from_deck(self, card):
        if isinstance(card, Plus4Card):
            plus_4_card = Plus4Card()
            return self.remove_card(plus_4_card)
        elif isinstance(card, ColorCard):
            color_card = ColorCard("All", "Colors")
            return self.remove_card(color_card)
        else:
            return self.remove_card(card)

    def remove_card(self, card):
        if card in self.deck:
            self.deck.remove(card)
            return True
        return False

    def show_cards_in_deck(self):
        if len(self.deck) == 0:
            return "No cards"
        card_string = "Cards in deck:\n| "
        for card in self.deck:
            card_string += str(card) + " | "
        return card_string