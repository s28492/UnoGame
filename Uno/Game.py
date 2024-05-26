"""
@author Cyprian Szewczak s2849
"""
import itertools
import random
from rich.console import Console
from Player import Player
import time
from rich import print
from Deck import Deck
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
        self.move_history = []
        self.round = 0
        self.ranking_table = [None for _ in args]
        self.deck = Deck()
        self.pile = []
        self.reset_colors = []
        self.card_on_top = None
        self.index_of_a_player = 0
        self.direction = 1
        self.turns_to_stop = 0
        self.cards_to_take = 0
        self.first_taken = False
        self.initialize_game()

    def get_card_on_top(self):
        return self.card_on_top

    def get_num_cards_left_in_deck(self):
        return self.deck.get_deck_len()

    def get_round(self):
        return self.round

    def get_direction(self):
        return self.direction

    def get_enemy_hand_num(self):
        return

    def get_state(self) -> tuple:
        """Returns bot data"""
        return self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take, self.first_taken

    def get_player(self) -> Player:
        """Returns current player"""
        return self.players[self.index_of_a_player]

    def get_next_player(self) -> Player:
        """Returns next player in line"""
        return self.players[(self.index_of_a_player + self.direction) % len(self.players)]

    @staticmethod
    def check_number_of_players(args) -> list:
        """Cheks correctness of initial number of players"""
        if len(args) < 2:
            raise ValueError("Sorry, You can't play alone")
        elif len(args) > 10:
            raise ValueError("You have too many friends to play this game")
        else:
            return [player for player in args]

    def deal_cards_to_players(self) -> None:
        """deals 7 cards for each player"""
        for player in self.players:
            for i in range(7):
                self.take_card(player)

    def initialize_game(self) -> None:
        """Initializes a game"""
        self.deal_cards_to_players()
        self.put_card(self.deck.draw_card())

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
        self.deck.cards_to_deck(player.hand)
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

    def take_card(self, player):
        """
        Gives a card from the deck to a player.
        If deck has less than 2 cards then it shuffles a pile into a deck before
        """
        if self.deck.deck_length() <= 1:
            if len(self.pile) > 1:
                self.reset_colored_cards()
                last_card = self.pile.pop()
                self.deck.extend(self.pile)
                self.pile = [last_card]
                self.shuffle_deck()
            else:
                return None
        card_drawed = self.deck.draw_card()
        player.hand.append(card_drawed)
        return card_drawed

    def move_pile_to_deck(self) -> None:
        """Moves cards from the pile to the deck exlcuding top card on pile"""
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

    def change_game_direction(self):
        self.direction *= -1

    def add_cards_to_take(self, how_many: int):
        self.cards_to_take += how_many

    def update_player_index(self) -> int:
        """changes current player list indicator"""
        return (self.index_of_a_player + self.direction) % len(self.players)

    def show_state(self, player) -> None:
        """Shows current player, card on top, players hand and state of the game"""
        self.console.print(f"{player}")
        self.console.print(f"Card on the top -> [{self.card_on_top.color.lower()}]{self.card_on_top}[/]")

        if self.cards_to_take != 0:
            self.console.print(f"Cards to take -> {self.cards_to_take}\nWrite Draw to take or play valid plus card.")
        elif self.turns_to_stop != 0:
            self.console.print(f"Turns to stop -> {self.turns_to_stop}\nWrite Stop to stop or play valid stop card.")

    def manage_stop(self, player, card):
        if card.value == "Stop" and card.color == "Stop":
            if self.turns_to_stop == 1:
                self.turns_to_stop = 0
                return True
            else:
                player.stop_player(self.turns_to_stop - 1)
                self.turns_to_stop = 0
                return True
        elif card.value == "Stop":
            self.turns_to_stop += 1
            player.play_card(card)
            self.put_card(card)
            return True
        return False

    def add_turns_to_stop(self):
        self.turns_to_stop += 1

    def manage_draw(self, player, first_card_taken=None):
        if not isinstance(first_card_taken, Card):
            first_card_taken = self.take_card(player)
            self.cards_to_take = self.cards_to_take - 1 if self.cards_to_take != 0 else 0


        if isinstance(first_card_taken, Card):
            if self.cards_to_take != 0 and self.is_valid_plus_card(first_card_taken):
                self.console.print(f"You have drawed {first_card_taken}. Do you want to put it? Write \"Draw\" if you want to take rest of the cards.")
                player_move = player.move()
                if isinstance(player_move, DrawCard):
                    for i in range(self.cards_to_take):
                        self.take_card(player)
                    self.cards_to_take = 0
                elif player_move.match(self.card_on_top) and player_move == first_card_taken:
                    player.play_card(first_card_taken)
                    self.put_card(first_card_taken.play(self))
                else:
                    self.manage_draw(player, first_card_taken=first_card_taken)
            elif self.cards_to_take == 0 and first_card_taken.match(self.card_on_top):
                self.console.print(f"You have drawed {first_card_taken}. Do you want to put it? Write \"Draw\" if you want to keep it and take {self.cards_to_take} remaining cards")
                player_move = player.move()
                if player_move == first_card_taken:
                    player.play_card(first_card_taken)
                    self.put_card(first_card_taken.play(self))
                elif isinstance(player_move, DrawCard):
                    return
                else:
                    self.console.print("You have to choose the card you have drawed or just write \"Draw\" if you want to keep it.")
                    self.manage_draw(player, first_card_taken=first_card_taken)
            else:
                for i in range(self.cards_to_take - 1):
                    self.take_card(player)
                self.cards_to_take = 0

    def is_valid_plus_card(self, card):
        if card.__class__ == self.card_on_top.__class__ or isinstance(card, Plus4Card):
            return True
        return False

    def manage_player_move(self, player):
        player.extract_features(self)
        self.show_state(player)

        card_played = player.move()
        if card_played.match(self.card_on_top):
            if self.turns_to_stop != 0:
                 if not self.manage_stop(player, card_played):
                    print("You have picked wrong card, try again.")
                    self.manage_player_move(player)
            elif self.cards_to_take != 0 and self.is_valid_plus_card(card_played):
                player.play_card(card_played)
                self.put_card(card_played.play(self))
            elif self.cards_to_take != 0 and not self.is_valid_plus_card(card_played) and not isinstance(card_played, DrawCard):
                print("You have picked wrong card, try again.")
                self.manage_player_move(player)
            elif isinstance(card_played, DrawCard):
                drawed_card = self.deck.draw_card()
                if isinstance(drawed_card, Card):
                    self.manage_draw(player)
            else:
                player.play_card(card_played)
                self.put_card(card_played.play(self))
        else:
            self.console.print(f"Card [{card_played.color.lower()}]{card_played}[/] doesn't match card on top: [{self.card_on_top.color.lower()}]{self.card_on_top}[/]. Try again")
            return self.manage_player_move(player)




    def play(self) -> None:
        """Main game method. Controls game flow"""
        while len(self.players) > 1:
            self.round += 1
            print("\n")
            player = self.get_player()
            # Checks if player is stopped
            if player.stopped:
                player.update_stop_status()
            else:
                self.manage_player_move(player)

            if player.has_won():
                self.drop_player(player, did_not_surrender=True)

            self.index_of_a_player = self.update_player_index()
        self.drop_player(self.players[0], did_not_surrender=True)
        # prints ranking
        for i, player in enumerate(self.ranking_table):
            self.console.print(f"Place {i + 1}: {player}")
