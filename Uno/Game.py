import itertools
import random

from UnoGame.Uno.Card import Player, Card, ReverseCard, ColorCard, StopCard


class Game:
    values = [f"{i}" for i in range(10)]
    colors = ["Red", "Green", "Blue", "Yellow"]

    def __init__(self, *args: Player):
        self.pile = None
        self.deck = self.create_deck()
        self.shuffle_deck()
        if 1 < len(args) <= 10:  # Warunek ilości graczy
            self.players = [player for player in args]
        else:
            raise ValueError("Sorry, the number of players is incorrect.")
        self.pile = []
        self.pile.append(self.deck.pop())
        self.current_card = self.pile[-1]
        self.deal_cards()
        self.player_index = 0
        self.direction = 1  # Kierunek gry

    def create_deck(self):
        deck = []
        special_cards = []
        for card in itertools.product(self.values, self.colors):
            deck.append(Card(card[0], card[1]))
            if card[0] != 0:
                deck.append(Card(card[0], card[1]))

        for card in itertools.product(["Reverse"], self.colors):
            deck.append(ReverseCard(card[0], card[1]))
            deck.append(ReverseCard(card[0], card[1]))

        for card in itertools.product(["Stop"], self.colors):
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))

        for i in range(8):  # Domyślnie 8
            deck.append(ColorCard("All", "Colors"))

        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        for player in self.players:
            for i in range(7):  # Karty startowe
                player.hand.append(self.deck.pop(0))

    def draw_card_from_deck(self, player: Player):
        if len(self.deck) == 0:
            self.deck = self.pile[:-1]
            random.shuffle(self.deck)
            self.pile = [self.pile[-1]]

        player.hand.append(self.deck.pop())

    def play_card(self, player):
        able_to_play_move = player.player_status()
        if able_to_play_move:
            move = player.play_move(self.current_card)
            if move.color == "Draw":
                self.draw_card_from_deck(player)
            elif move.value == "Stopped":
                return
            elif move.color == "Surrender":
                self.players.remove(player)
            else:
                while not move.match(self.current_card):
                    print("You can't put this card here")
                    player.hand.append(move)
                    return self.play_card(player)

                self.current_card = move.play(self, player)
                self.pile.append(self.current_card)
                print(f"Card played: | {move} |")
        return

    def play(self):
        winner = None
        while winner is None:
            players_amount = len(self.players)
            self.player_index %= players_amount
            player = self.players[self.player_index]
            if player.stopped:
                player.manage_stop()
            else:
                self.play_card(player)
                if len(player.hand) == 0:
                    winner = player
                if len(self.players) == 1:
                    winner = self.players[0]
                self.player_index += self.direction
        print(f"Congratulations {winner}. You won the game!!!")

