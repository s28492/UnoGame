import itertools
import random


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"

    def __eq__(self, other):
        if (self.value == other.value) and (self.color == other.color):
            return True
        else:
            return False


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name

    def show_hand(self):
        cards = f"{self.name} hand:\n| "
        for card in self.hand:
            cards += f"{card} | "
        return cards

    def draw(self, card):
        self.hand.append(card)

    def play_card(self):
        print(self.show_hand())
        print("Write whitch card you wanna play:")
        value = input()
        card = value.split(" ")
        card = Card(int(card[0]), card[1])
        if card in self.hand:
            self.hand.pop(self.hand.index(card))
            print(f"Wyłożono: | {card} |")
        else:
            print("It seems that you don't have this card on hand. Let's try again:")
            self.play_card()
        # return self.hand.pop()


class Game:
    values = [i for i in range(10)]
    colors = ["Red", "Green", "Blue", "Yellow"]

    def __init__(self, *args: Player):
        self.deck = self.create_deck()
        self.shuffle_deck()
        if 1 < len(args) <= 10:             # Warunek ilości graczy
            self.players = args
        else:
            raise ValueError("Sorry, the number of players is incorrect.")
        self.pile = [].append(self.deck.pop(0))
        self.deal_cards()
        self.direction = 1  # Kierunek gry

    def create_deck(self):
        deck = []
        for card in itertools.product(self.values, self.colors):
            deck.append(Card(card[0], card[1]))
            if card[0] != 0:
                deck.append(Card(card[0], card[1]))
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        for player in self.players:
            for i in range(7):
                player.draw(self.deck.pop(0))

    def play(self):
        winner = None
        while(winner == None):
            for player in self.players:
                #print(player.show_hand())
                player.play_card()
                if len(player.hand) == 0:
                    winner = player
                    break
        print(f"Gratulacje {winner}")



class ReverseCard(Card):
    # Specjalne zachowanie dla karty Reverse
    pass


class StopCard(Card):
    pass


class Plus2Card(Card):
    pass


class Plus4Card(Card):
    TAKE4 = 4
    pass
