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

    def play_move(self, top_card_on_pile):
        print(f"Card on the top of the pile: {top_card_on_pile}")
        print(self.show_hand())
        print("Write what you wanna play: [Value Color], [Draw], [Surrender]")
        value = input()

        if value == "Draw":
            value = "-1 Draw"
        elif value == "Surrender":
            value = "-1 Surrender"
        card = value.split(" ")
        try:
            card = Card(int(card[0]), card[1])
        except:
            print("You gave me wrong values you sneaky bastard!")
            return self.play_move(top_card_on_pile)
        if card.value == "Draw" or card.value == "Surrender":
            return card
        elif card in self.hand:
            self.hand.remove(card)
            return card
        else:
            print("It seems that you don't have this card on hand. Let's try again:")
            return self.play_move(top_card_on_pile)
        # return self.hand.pop()


class Game:
    values = [i for i in range(10)]
    colors = ["Red", "Green", "Blue", "Yellow"]

    def __init__(self, *args: Player):
        self.deck = self.create_deck()
        self.shuffle_deck()
        if 1 < len(args) <= 10:  # Warunek ilości graczy
            self.players = [player for player in args]
        else:
            raise ValueError("Sorry, the number of players is incorrect.")
        self.pile = self.deck.pop()
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
            for i in range(7):  # Karty startowe
                player.draw(self.deck.pop(0))

    def draw_card(self, player: Player):
        if len(self.deck) > 0:

            player.draw(self.deck.pop(0))
        else:
            print("Deck is empty, you have to go on without one.")

    def play(self):
        winner = None
        player_index = 0
        players_amount = len(self.players)
        while winner is None:
            player = self.players[player_index % players_amount]
            move = player.play_move(self.pile)
            if move.value == "Draw":
                self.draw_card(player)
            elif move.value == "Surrender":
                self.players.remove(player)
                break
            else:
                while move.value != self.pile.value and move.color != self.pile.color:
                    print("You can't put this card here")
                    move = player.play_move(self.pile)
                self.pile = move
                print(f"Card played: | {move} |")
            if len(player.hand) == 0:
                winner = player
            if len(self.players) == 1:
                winner = self.players[0]
            player_index += self.direction
        print(f"Congratulations {winner}. You won the game!!!")


class ReverseCard(Card):
    # Specjalne zachowanie dla karty Reverse
    def __init__(self, color, value):
        super().__init__(color, value)

    pass


class StopCard(Card):
    def __init__(self, color, value):
        super().__init__(color, value)


class Plus2Card(Card):
    def __init__(self, color, value):
        super().__init__(color, value)


class Plus4Card(Card):
    def __init__(self, color, value):
        super().__init__(color, value)


class ColorCard(Card):
    def __init__(self, color, value):
        super().__init__(color, value)
