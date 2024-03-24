import itertools
import random

from Card import Card, StopCard, Plus2Card, Plus4Card, ColorCard, ReverseCard


class Game:
    colors = ["Red", "Green", "Blue", "Yellow"]
    values = [f"{i}" for i in range(10)]

    def __init__(self, *args: Player):
        self.players = self.check_number_of_players(args)
        self.ranking_table = [None for _ in args]
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.pile = []
        self.card_on_top = None
        self.index_of_a_player = 0
        self.direction = 1
        self.turns_to_stop = 0
        self.cards_to_take = 0
        self.initialize_game()

    def get_player(self):
        return self.players[self.index_of_a_player]
    @staticmethod
    def check_number_of_players(args):
        if len(args) < 2:
            raise ValueError("Sorry, You can't play alone")
        elif len(args) > 10:
            raise ValueError("You have to many friends to play this game")
        else:
            return [player for player in args]

    def create_deck(self):
        deck = []
        for card in itertools.product(self.values, self.colors):  # Po 19 na kolor
            deck.append(Card(card[0], card[1]))
            if card[0] != 0:
                deck.append(Card(card[0], card[1]))

        for card in itertools.product(["Reverse"], self.colors):  # Po 2 na kolor
            deck.append(ReverseCard(card[0], card[1]))
            deck.append(ReverseCard(card[0], card[1]))

        for card in itertools.product(["Stop"], self.colors):  # Po 2 na kolor
            deck.append(StopCard(card[0], card[1]))
            deck.append(StopCard(card[0], card[1]))

        for card in itertools.product(["+2"], self.colors):  # Po 2 na kolor
            deck.append(Plus2Card(card[0], card[1]))
            deck.append(Plus2Card(card[0], card[1]))

        for card in itertools.product(["+4"], self.colors):  # Po 1 na kolor
            deck.append(Plus4Card(card[0], card[1]))

        for i in range(8):  # Po 1 na kolor
            deck.append(ColorCard("All", "Colors"))

        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards_to_players(self):
        for player in self.players:
            for i in range(7):
                self.take_card(player)

    def initialize_game(self):
        self.deal_cards_to_players()
        self.put_card(self.deck.pop(0))

    def put_card(self, card):
        self.pile.append(card)
        self.card_on_top = card

    def empty_hand(self, player):
        if len(player.hand) == 0:
            self.drop_player(player, did_not_surrender=True)
            print(f"Congratulations {player}. You have finished the game")

    def drop_player(self, player, did_not_surrender=False):

        if did_not_surrender:
            for i in range(len(self.ranking_table)):
                if self.ranking_table[i] is None:
                    self.ranking_table[i] = self.players.pop(self.players.index(player))
                    break
        else:
            for i in range(len(self.ranking_table) - 1, 0, -1):
                if self.ranking_table[i] is None:
                    self.ranking_table[i] = self.players.pop(self.players.index(player))
                    break
        self.index_of_a_player -= 1

    def take_card(self, player):
        if len(self.deck) <= 1:
            for i in range(len(self.pile) - 1):
                self.deck.append(self.pile.pop(i))
            self.shuffle_deck()
        player.hand.append(self.deck.pop(0))

    def wanna_stop(self, player):
        print(f"Turns to stop -> {self.turns_to_stop}\nDo you wanna stop? [Yes/No]")
        decision = self.player_decision()
        if decision == "Yes":
            player.stop_status, self.turns_to_stop = self.turns_to_stop - 1, 0
            if player.stop_status > 0:
                player.stopped = True
        else:
            player.show_hand()
            card = player.move()
            if isinstance(card, StopCard):
                self.turns_to_stop += 1
                self.empty_hand(player)
            else:
                print("You played wrong card you bastard. Try again")
                return self.wanna_stop(player)

    @staticmethod
    def player_decision():
        decision = input()
        while decision not in ["Yes", "No"]:
            decision = input("Sorry wrong input. Try again")
        return decision

    def is_valid_plus_card(self, card: Card):
        print(f"Karta: {card} -> typ: {type(card)} -> value {card.value}")
        print(f"Self: {self.card_on_top} -> typ: {type(self.card_on_top)}-> value {self.card_on_top.value}")

        if (card.match(self.card_on_top) and self.cards_to_take == 0) or (
                self.cards_to_take != 0 and (card.value == self.card_on_top.value or card.value == "+4")):
            return True
        return False

    def take_first_card(self, player):
        first_taken = self.deck.pop(0)
        player.hand.append(first_taken)
        if self.is_valid_plus_card(first_taken):
            print(f"You draw {first_taken}\nDo you wanna put it? [Yes/No]")
            put_card_decision = self.player_decision()
            if put_card_decision == "Yes":
                card_to_put = first_taken.play(self)
                self.put_card(card_to_put)
                return True
            else:
                return False
        return False

    def wanna_take(self, player):
        print(f"Cards to take -> {self.cards_to_take}\nDo you wanna take? [Yes/No]")
        decision = self.player_decision()
        if decision == "Yes":
            first_putted = self.take_first_card(player)
            if not first_putted:
                for i in range(self.cards_to_take - 1):
                    self.take_card(player)
                self.cards_to_take = 0
        else:
            player.show_hand()
            card = player.move()
            if self.is_valid_plus_card(card):
                card_to_put = card.play(self)
                self.put_card(card_to_put)
                self.empty_hand(player)
            else:
                print("You played wrong card you bastard. Try again")
                return self.wanna_take(player)

    def player_index(self):
        return (self.index_of_a_player + self.direction) % len(self.players)

    def show_state(self, player):

        print(f"{player}")
        print(f"Card on the top -> {self.card_on_top}")
        player.show_hand()

    def normal_move(self, player):
        card_played = player.move()
        if card_played.match(self.card_on_top):
            card_to_put = card_played.play(self)
            self.put_card(card_to_put)
            self.empty_hand(player)
        else:
            print("You can't put this card here. Try again")
            return self.normal_move(player)


    def play(self):
        while len(self.players) > 1:
            print(self.index_of_a_player)
            player = self.players[self.index_of_a_player]
            if player.stopped:
                player.stop_status -= 1
                if player.stop_status == 0:
                    player.stopped = False
            elif self.turns_to_stop != 0:
                self.show_state(player)
                self.wanna_stop(player)
            elif self.cards_to_take != 0:
                self.show_state(player)
                self.wanna_take(player)
            else:
                self.show_state(player)
                self.normal_move(player)

            self.index_of_a_player = self.player_index()
        self.drop_player(self.players[0], did_not_surrender=True)
        for i, player in enumerate(self.ranking_table):
            print(f"Place {i + 1}: {player}")
