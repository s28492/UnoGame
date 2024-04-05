import itertools
import random
from rich.console import Console
from Player import Player
import time

from Card import Card, StopCard, Plus2Card, Plus4Card, ColorCard, ReverseCard, DrawCard


class Game:
    # console = Console()
    colors = ["Red", "Green", "Blue", "Yellow"]
    values = [i for i in range(10)]

    def __init__(self, *args: Player):
        self.console = Console()
        self.players = self.check_number_of_players(args)
        self.ranking_table = [None for _ in args]
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.pile = []
        self.reset_colors = []
        self.card_on_top = None
        self.index_of_a_player = 0
        self.direction = 1
        self.turns_to_stop = 0
        self.cards_to_take = 0
        self.initialize_game()

    def get_bot_data(self):
        return self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take

    def get_player(self):  # Returns current player
        return self.players[self.index_of_a_player]

    @staticmethod
    def check_number_of_players(args):  # Cheks correctness of initial number of players
        if len(args) < 2:
            raise ValueError("Sorry, You can't play alone")
        elif len(args) > 10:
            raise ValueError("You have too many friends to play this game")
        else:
            return [player for player in args]

    def create_deck(self):  # Creates deck
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

        for i in range(4):  # Po 1 na kolor
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
            self.console.print(f"Congratulations {player}. You have finished the game", style="rgb(255,215,0)")

    def drop_player(self, player: Player, did_not_surrender=False):
        for card in player.hand:
            self.deck.append(card)
        player.hand = []
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
            if len(self.pile) > 1:
                self.reset_colored_cards()
                last_card = self.pile.pop()
                self.deck.extend(self.pile)
                self.pile = [last_card]
                self.shuffle_deck()
            else:
                return
        player.hand.append(self.deck.pop(0))

    def move_pile_to_deck(self):
        if len(self.pile) > 1:
            self.reset_colored_cards()
            last_card = self.pile.pop()
            self.deck.extend(self.pile[:-1])
            self.pile = [last_card]
            self.shuffle_deck()

    def reset_colored_cards(self):
        for card in self.pile:
            if isinstance(card, ColorCard):
                card.color = "Color"

    def is_valid_card(self, card: Card):  # Checks if given card can be put on other plsu cards
        if (card.match(self.card_on_top) and self.cards_to_take == 0) or (
                self.cards_to_take != 0 and (card.value == self.card_on_top.value or card.value == "+4")):
            return True
        return False

    def take_first_card(self, player):  # takes first card from deck and then checks if it can be played instantly
        if len(self.deck) > 0:
            first_taken = self.deck.pop(0)
            player.hand.append(first_taken)
            if self.is_valid_card(first_taken):
                self.console.print(
                    f"You draw: [{first_taken.color.lower()}]{first_taken}[/]\nDo you wanna put it? [bold][Yes/No][/]")
                put_card_decision = player.player_decision()
                if put_card_decision == "Yes":
                    card_to_put = first_taken.play(self)
                    self.put_card(card_to_put)
                    return True
                else:
                    return False
            return False
        else:
            self.move_pile_to_deck()
            self.take_first_card(player)

    def wanna_stop(self, player):  # Checks if player wants to stop or play another stop card
        self.console.print(f"Turns to stop -> {self.turns_to_stop}\nDo you wanna stop? [Yes/No]")
        decision = player.player_decision()
        if decision == "Yes":
            self.console.print("Player stopped...", style="rgb(122,3,4)")
            player.stop_status, self.turns_to_stop = self.turns_to_stop - 1, 0
            if player.stop_status > 0:
                player.stopped = True
        else:
            player.show_hand()
            card = player.move()
            if isinstance(card, StopCard):
                card.play(self)
                self.put_card(card)
                self.empty_hand(player)
            else:
                self.console.print("You played wrong card you bastard. Try again")
                return self.wanna_stop(player)

    def wanna_take(self, player):  # Asks player if either wants to take cards or add another plus card
        self.console.print(f"Cards to take -> {self.cards_to_take}\nDo you wanna take? [Yes/No]")
        decision = player.player_decision()
        if decision == "Yes":
            first_putted = self.take_first_card(player)
            if not first_putted:
                for i in range(self.cards_to_take - 1):
                    self.take_card(player)
                self.cards_to_take = 0
        else:
            player.show_hand()
            card = player.move()
            if self.is_valid_card(card):
                if isinstance(card, DrawCard):
                    self.console.print(f"{player} drawed a card")
                    card.play(self)
                else:
                    card_to_put = card.play(self)
                    self.console.print(f"Card played: [{card.color}]{card}")
                    self.put_card(card_to_put)
                    self.empty_hand(player)
            else:
                self.console.print("You played wrong card you bastard. Try again")
                return self.wanna_take(player)

    def update_player_index(self):  # changes current player indicator with
        return (self.index_of_a_player + self.direction) % len(self.players)

    def show_state(self, player):

        self.console.print(f"{player}")
        self.console.print(f"Card on the top -> [{self.card_on_top.color.lower()}]{self.card_on_top}[/]")
        player.show_hand()

    def normal_move(self, player):
        card_played = player.move()
        if card_played.match(self.card_on_top):
            card_to_put = card_played.play(self)
            if isinstance(card_played, DrawCard):
                self.console.print(f"{player} drawed a card")
            else:
                self.console.print(f"card played: [{card_to_put.color.lower()}]{str(card_to_put)}[/]")
                self.put_card(card_to_put)
                self.empty_hand(player)
        else:
            print("You can't put this card here. Try again")
            return self.normal_move(player)

    def play(self):
        while len(self.players) > 1:
            print("\n")
            player = self.get_player()
            time.sleep(0.1)
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

            self.index_of_a_player = self.update_player_index()
        self.drop_player(self.players[0], did_not_surrender=True)
        for i, player in enumerate(self.ranking_table):
            self.console.print(f"Place {i + 1}: {player}")