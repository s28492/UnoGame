"""
@author Cyprian Szewczak s2849
"""
import itertools
import random
from rich.console import Console
from Player import Player
import time

from Card import Card, StopCard, Plus2Card, Plus4Card, ColorCard, ReverseCard, DrawCard


class Game:
    colors = ["Red", "Green", "Blue", "Yellow"]
    values = [i for i in range(10)]
    # transposes int values to str values
    values = map(lambda val: str(val), values)

    def __init__(self, *args: Player):
        """Initialize game start state"""
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

    def get_bot_data(self) -> tuple:
        """Returns bot data"""
        return self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take

    def get_player(self) -> Player:
        """Returns current player"""
        return self.players[self.index_of_a_player]

    @staticmethod
    def check_number_of_players(args) -> list:
        """Cheks correctness of initial number of players"""
        if len(args) < 2:
            raise ValueError("Sorry, You can't play alone")
        elif len(args) > 10:
            raise ValueError("You have too many friends to play this game")
        else:
            return [player for player in args]

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

        for card in itertools.product(["+2"], self.colors):  # 2 for each color
            deck.append(Plus2Card(card[0], card[1]))
            deck.append(Plus2Card(card[0], card[1]))

        for card in itertools.product(["+4"], self.colors):  # 1 for each color
            deck.append(Plus4Card(card[0], card[1]))

        for i in range(4):  # 1 for each color
            deck.append(ColorCard("All", "Colors"))
        return deck

    def shuffle_deck(self) -> None:
        """shuffles the deck"""
        random.shuffle(self.deck)

    def deal_cards_to_players(self) -> None:
        """deals 7 cards for each player"""
        for player in self.players:
            for i in range(7):
                self.take_card(player)

    def initialize_game(self) -> None:
        """Initializes a game"""
        self.deal_cards_to_players()
        self.put_card(self.deck.pop(0))

    def put_card(self, card) -> None:
        """Puts first card on pile"""
        self.pile.append(card)
        self.card_on_top = card

    def empty_hand(self, player) -> None:
        """Checks if hand is empty. If yes, the player has finished and is removed from players list"""
        if len(player.hand) == 0:
            self.drop_player(player, did_not_surrender=True)
            self.console.print(f"Congratulations {player}. You have finished the game", style="rgb(255,215,0)")

    def drop_player(self, player: Player, did_not_surrender=False) -> None:
        """Removes player from players list
        If player did_not_surrender he is added to first empty slot from the beggining
        If player did_not_surrender = False he is added to first empty slot from the end
        """
        for card in player.hand:
            self.deck.append(card)
        player.hand = []
        # If didn't surrender
        if did_not_surrender:
            for i in range(len(self.ranking_table)):
                if self.ranking_table[i] is None:
                    self.ranking_table[i] = self.players.pop(self.players.index(player))
                    break
        # If surrender
        else:
            for i in range(len(self.ranking_table) - 1, 0, -1):
                if self.ranking_table[i] is None:
                    self.ranking_table[i] = self.players.pop(self.players.index(player))
                    break
        self.index_of_a_player -= 1

    def take_card(self, player) -> None:
        """
        Gives a card from the deck to a player.
        If deck has less than 2 cards then it shuffles a pile into a deck before
        """
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

    def move_pile_to_deck(self) -> None:
        """Moves cards from the pile to the deck exluding top card on pile"""
        if len(self.pile) > 1:
            self.reset_colored_cards()
            last_card = self.pile.pop()
            self.deck.extend(self.pile[:-1])
            self.pile = [last_card]
            self.shuffle_deck()

    def reset_colored_cards(self) -> None:
        """Resets Colored cards being moved to the deck from pile"""
        for card in self.pile:
            if isinstance(card, ColorCard):
                card.color = "Color"

    def is_valid_card(self, card: Card) -> bool:
        """Checks if given card can be put on other plsu cards"""
        valid_if_zero_to_take = card.match(self.card_on_top) and self.cards_to_take == 0
        valid_if_want_to_counter_taking = self.cards_to_take != 0 and (
                    card.value == self.card_on_top.value or card.value == "+4")
        if valid_if_zero_to_take or valid_if_want_to_counter_taking:
            return True
        return False

    def take_first_card(self, player) -> bool:
        """
        takes first card from deck and then checks if it can be played instantly.
        returns a bool
        """
        if len(self.deck) > 0:
            first_taken = self.deck.pop(0)
            player.hand.append(first_taken)
            # Checks if card can be played
            if self.is_valid_card(first_taken):
                self.console.print(
                    f"You draw: [{first_taken.color.lower()}]{first_taken}[/]\nDo you wanna put it? [bold][Yes/No][/]")
                # Asks a player if he wants to play it
                put_card_decision = player.player_decision()
                if put_card_decision == "Yes":
                    card_to_put = first_taken.play(self)
                    self.console.print(f"card played: [{card_to_put.color.lower()}]{card_to_put}")
                    self.put_card(card_to_put)
                    return True
                else:
                    return False
            return False
        else:
            self.move_pile_to_deck()
            self.take_first_card(player)

    def wanna_stop(self, player) -> None:
        """Checks if player wants to stop or play another stop card"""
        self.console.print(f"Turns to stop -> {self.turns_to_stop}\nDo you wanna stop? [Yes/No]")
        decision = player.player_decision()
        if decision == "Yes":
            self.console.print("Player stopped...", style="rgb(122,3,4)")
            # Update player stop status and turns to stop
            player.stop_status, self.turns_to_stop = self.turns_to_stop - 1, 0
            if player.stop_status > 0:
                player.stopped = True
        else:
            player.show_hand()
            card = player.move()
            # Checks if stop card was played, if not returns to the beginning of a method
            if isinstance(card, StopCard):
                card.play(self)
                self.put_card(card)
                self.empty_hand(player)
            else:
                self.console.print("You played wrong card you bastard. Try again")
                return self.wanna_stop(player)

    def wanna_take(self, player) -> None:
        """Asks player if either wants to take cards or add another plus card"""
        self.console.print(f"Cards to take -> {self.cards_to_take}\nDo you wanna take? [Yes/No]")
        decision = player.player_decision()
        if decision == "Yes":
            # Checks if first drawed card could be placed instantly
            first_putted = self.take_first_card(player)
            # If not it draws the rest of cards
            if not first_putted:
                for i in range(self.cards_to_take - 1):
                    self.take_card(player)
                self.cards_to_take = 0
        else:
            # player makes a move
            player.show_hand()
            card = player.move()
            # Checks if move is valid
            if self.is_valid_card(card):
                card_to_put = card.play(self)
                self.console.print(f"Card played: [{card.color}]{card}")
                self.put_card(card_to_put)
                self.empty_hand(player)
            else:
                self.console.print("You played wrong card you bastard. Try again")
                return self.wanna_take(player)

    def update_player_index(self) -> int:
        """changes current player list indicator"""
        return (self.index_of_a_player + self.direction) % len(self.players)

    def show_state(self, player) -> None:
        """Shows current player, card on top, and players hand"""
        self.console.print(f"{player}")
        self.console.print(f"Card on the top -> [{self.card_on_top.color.lower()}]{self.card_on_top}[/]")
        player.show_hand()

    def normal_move(self, player) -> None:
        """takes player move and checks its correctness with top card"""
        card_played = player.move()
        if card_played.match(self.card_on_top):
            # Plays a card
            card_to_put = card_played.play(self)
            # Draws a card
            if isinstance(card_played, DrawCard):
                self.console.print(f"{player} drawed a card")
            else:
                # puts card on top and erases it from players hand
                self.console.print(f"card played: [{card_to_put.color.lower()}]{str(card_to_put)}[/]")
                self.put_card(card_to_put)
                self.empty_hand(player)
        else:
            print("You can't put this card here. Try again")
            return self.normal_move(player)

    def play(self) -> None:
        """Main game method. Controls game flow"""
        while len(self.players) > 1:
            print("\n")
            player = self.get_player()
            time.sleep(0.8)
            # Checks if player is stopped
            if player.stopped:
                player.stop_status -= 1
                if player.stop_status == 0:
                    player.stopped = False
            # Checks if turns to stop is not 0
            elif self.turns_to_stop != 0:
                self.show_state(player)
                self.wanna_stop(player)
            # Checks take status
            elif self.cards_to_take != 0:
                self.show_state(player)
                self.wanna_take(player)
            # Player can make a normal move
            else:
                self.show_state(player)
                self.normal_move(player)

            self.index_of_a_player = self.update_player_index()
        self.drop_player(self.players[0], did_not_surrender=True)
        # prints ranking
        for i, player in enumerate(self.ranking_table):
            self.console.print(f"Place {i + 1}: {player}")
