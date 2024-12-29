import uuid

from Uno.players.Player import Player
from Uno.game.Deck import Deck
from Uno.game.Card import Card
from rich.console import Console


class GameState:
    """
    Encapsulates the game's state data.
    """

    def __init__(self, players: list, is_simulation=False):
        """Initialize game start state"""
        self.console = Console()
        self.game_id = str(uuid.uuid4())
        self.players: list[Player] = self._check_number_of_players(players)
        self.move_history = []
        self.round = 0
        self.ranking_table = [None for _ in players]
        self.deck = Deck()
        self.pile: list[Card] = []
        self.reset_colors = []
        self.card_on_top = None
        self.index_of_a_player = 0
        self.direction = 1
        self.turns_to_stop = 0
        self.cards_to_take = 0
        self.first_taken = False
        self.game_over = False
        self.features_list = []
        self.deal_cards_to_players()
        self.is_simulation = is_simulation

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    def set_features_list(self, features_list):
        self.features_list = features_list

    def get_features_list(self):
        return self.features_list

    def set_reset_colors(self, reset_colors):
        self.reset_colors = reset_colors

    def set_round(self, round):
        self.round = round

    def get_round(self):
        return self.round

    def set_ranking_table(self, ranking_table):
        self.ranking_table = ranking_table

    def get_ranking_table(self):
        return self.ranking_table

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck

    def set_pile(self, pile):
        self.pile = pile

    def get_pile(self):
        return self.pile

    def set_card_on_top(self, card_on_top):
        self.card_on_top = card_on_top

    def get_card_on_top(self):
        return self.card_on_top

    def set_index_of_a_player(self, index_of_a_player):
        self.index_of_a_player = index_of_a_player

    def get_index_of_a_player(self):
        return self.index_of_a_player

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def set_turns_to_stop(self, turns_to_stop):
        self.turns_to_stop = turns_to_stop

    def get_turns_to_stop(self):
        return self.turns_to_stop

    def set_cards_to_take(self, cards_to_take):
        self.cards_to_take = cards_to_take

    def get_cards_to_take(self):
        return self.cards_to_take

    def set_first_taken(self, first_taken):
        self.first_taken = first_taken

    def get_first_taken(self):
        return self.first_taken

    def set_game_over(self, game_over):
        self.game_over = game_over

    def get_game_over(self):
        return self.game_over

    @staticmethod
    def _check_number_of_players(players) -> list[Player]:
        """Cheks correctness of initial number of players"""
        if len(players) < 2:
            raise ValueError("Sorry, You can't play alone")
        elif len(players) > 10:
            raise ValueError("You have too many friends to play this game")
        else:
            return [player for player in players]

    def deal_cards_to_players(self) -> None:
        """deals 7 cards for each player"""
        for player in self.players:
            for i in range(7):
                self.take_card(player)

    def put_card(self, card) -> None:
        """Puts first card on pile"""
        self.pile.append(card)
        self.card_on_top = card

    def take_card(self, player):
        """
        Gives a card from the deck to a player.
        If deck has less than 2 cards then it shuffles a pile into a deck before
        """
        if self.deck.deck_length() <= 1:
            if len(self.pile) > 1:
                last_card = self.pile.pop(-1)
                self.deck.reshuffle_discard_pile(self.pile)
                self.pile = [last_card]
            else:
                return None
        card_drawed = self.deck.draw_card()
        player.hand.append(card_drawed)
        return card_drawed

    def move_pile_to_deck(self) -> None:
        """Moves cards from the pile to the deck exlcuding top card on pile"""
        if len(self.pile) > 1:
            last_card = self.pile.pop(-1)
            self.deck.reshuffle_discard_pile(self.pile)
            self.pile = [last_card]

    def get_card_on_top(self):
        return self.card_on_top

    def get_num_cards_left_in_deck(self):
        return self.deck.get_deck_len()

    def get_round(self):
        return self.round

    def get_pile(self):
        return self.pile

    def get_direction(self):
        return self.direction

    def get_game_over(self):
        return self.game_over

    def get_state(self) -> tuple:
        """Returns bot data"""
        return self.players, self.pile, self.card_on_top, self.direction, self.turns_to_stop, self.cards_to_take, self.first_taken

    def get_player(self) -> Player:
        """Returns current player"""
        return self.players[self.index_of_a_player]

    def get_next_player(self) -> Player:
        """Returns next player in line"""
        return self.players[(self.index_of_a_player + self.direction) % len(self.players)]

    def get_players(self):
        return self.players

    def update_player_index(self) -> int:
        """changes current player list indicator"""
        return (self.index_of_a_player + self.direction) % len(self.players)

    def show_num_of_cards_for_all(self):
        messege = ""
        for player in self.players:
            messege += f"{player.rich_str()}: {len(player.hand)} | "
        return messege

    def add_cards_to_take(self, how_many: int):
        self.cards_to_take += how_many

    def change_game_direction(self):
        self.direction *= -1

    def add_turns_to_stop(self):
        self.turns_to_stop += 1

    def drop_player(self, player: Player, did_not_surrender=False) -> None:
        """Removes player from players list
        If player did_not_surrender he is added to first empty slot from the beggining
        If player did_not_surrender = False he is added to first empty slot from the end
        """
        self.deck.cards_to_deck(player.hand)
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

    def show_state(self, player) -> None:
        """Shows current player, card on top, players hand and state of the game"""
        self.console.print("\n\n")
        self.console.print(f"{player.rich_str()}")
        self.console.print(f"Card on the top -> [{self.card_on_top.color.lower()}]{self.card_on_top}[/]")
        self.console.print(self.show_num_of_cards_for_all())
        if self.cards_to_take != 0:
            self.console.print(f"Cards to take -> {self.cards_to_take}\nWrite Draw to take or play valid plus card.")
        elif self.turns_to_stop != 0:
            self.console.print(f"Turns to stop -> {self.turns_to_stop}\nWrite Stop to stop or play valid stop card.")

    def empty_hand(self, player) -> None:
        """Checks if hand is empty. If yes, the player has finished and is removed from players list"""
        if len(player.hand) == 0:
            self.drop_player(player, did_not_surrender=True)

    def check_number_of_cards_in_game(self):
        sum = 0
        for player in self.players:
            sum += len(player.hand)
        num_of_cards = len(self.deck.deck) + len(self.pile) + sum

        if num_of_cards != 108:
            if self.is_simulation:
                print("SIMULATION ERROR")
                print("Pile: ", len(self.pile))
                for card in self.pile:
                    print(card)
                print("Deck: ", len(self.deck.deck))
                print("players: ", sum)
            raise ValueError(f"Not enough cards in deck or pile. Expected 108, got {num_of_cards}")

    def reset_all_bots(self):
        for player in self.players:
            if isinstance(player, Bot):
                del player

    def show_infinite_mistakes(self):
        print("Game too long")
        self.show_state(self.get_player())
        print(f"ID3 hand len {len(self.get_player().hand)}")
        print(f"Cards in deck {len(self.deck.deck)}")
        print(f"Cards on pile {len(self.pile)}")

    def get_features_list(self):
        return self.features_list

    def set_game_over(self):
        self.game_over = True

