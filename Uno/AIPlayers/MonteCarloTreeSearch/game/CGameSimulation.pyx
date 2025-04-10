# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

from Uno.players.Bot import Bot
from Uno.AIPlayers import BaseAIBot
from Uno.game.Card import Card, Plus4Card, DrawCard, ColorCard
from Uno.game.GameState import GameState

cdef class GameSimulation:
    """
    Manages the game logic and interactions with GameState.
    """

    # Deklaracje atrybutów w klasie cdef
    cdef object game_state       # lub cdef GameState game_state (jeśli masz cimport do GameState)
    cdef bint show_game

    def __init__(self, list players, bint show_game=False):
        self.game_state = GameState(players, is_simulation=True)
        self.initialize_game()
        self.show_game = show_game  # przypisanie do cdef bint

    cpdef set_game_state(self, game_state):
        self.game_state = game_state

    cpdef initialize_game(self):
        """Initializes a game"""
        self.game_state.put_card(self.game_state.deck.draw_card())

    cpdef get_game_state(self):
        return self.game_state

    cpdef bint manage_stop(self, player, card):
        """
        Handles the logic of stop card and updating turns to stop variable.
        """
        if card.value == "Stop" and card.color == "Stop":
            if self.game_state.turns_to_stop == 1:
                self.game_state.turns_to_stop = 0
                return True
            else:
                player.stop_player(self.game_state.turns_to_stop - 1)
                self.game_state.turns_to_stop = 0
                return True
        elif card.value == "Stop":
            self.game_state.add_turns_to_stop()
            player.play_card(card)
            self.game_state.put_card(card)
            return True
        return False

    cpdef manage_draw(self, player, first_card_taken=None):
        cdef int i

        if first_card_taken is None:
            first_card_taken = self.game_state.take_card(player)
            if self.game_state.cards_to_take != 0:
                self.game_state.cards_to_take -= 1

        if self.game_state.cards_to_take != 0 and self.is_valid_plus_card(first_card_taken):
            if not isinstance(self.game_state.get_player(), Bot):
                self.game_state.console.print(
                    f"You have drawed {first_card_taken.rich_str()}. "
                    f"Do you want to put it? Write \"Draw\" if you want to take rest of the cards."
                )
            player_move = player.move(first_card_taken)
            if isinstance(player_move, DrawCard):
                for i in range(self.game_state.cards_to_take):
                    self.game_state.take_card(player)
                self.game_state.cards_to_take = 0
            elif (
                player_move.match(self.game_state.card_on_top) and
                player_move == first_card_taken
            ) or (
                isinstance(first_card_taken, ColorCard) and
                first_card_taken.value == player_move.value
            ):
                player.play_card(player_move)
                self.game_state.put_card(player_move.play(self.game_state))
            else:
                self.manage_draw(player, first_card_taken=first_card_taken)

        elif (
            self.game_state.cards_to_take == 0 and
            first_card_taken is not None and
            first_card_taken.match(self.game_state.card_on_top)
        ):
            if not isinstance(self.game_state.get_player(), Bot):
                self.game_state.console.print(
                    f"You have drawed {first_card_taken.rich_str()}. "
                    f"Do you want to put it? Write \"Draw\" if you want to keep it and take "
                    f"{self.game_state.cards_to_take} remaining cards"
                )
            player_move = player.move(first_card_taken)
            if (
                player_move == first_card_taken or
                (isinstance(first_card_taken, ColorCard) and first_card_taken.value == player_move.value)
            ):
                player.play_card(player_move)
                self.game_state.put_card(player_move.play(self.game_state))
            elif isinstance(player_move, DrawCard):
                return
            else:
                if not isinstance(self.game_state.get_player(), Bot):
                    self.game_state.console.print(
                        "You have to choose the card you have drawed or just write \"Draw\" if you want to keep it."
                    )
                self.manage_draw(player, first_card_taken=first_card_taken)
        else:
            for i in range(self.game_state.cards_to_take):
                self.game_state.take_card(player)
            self.game_state.cards_to_take = 0

    cpdef bint is_valid_plus_card(self, card):
        if card.__class__ == self.game_state.card_on_top.__class__ or isinstance(card, Plus4Card):
            return True
        return False

    cpdef update_bot(self, bot):
        if isinstance(bot, Bot):
            data_for_bot = (
                self.game_state.get_players(),
                self.game_state.pile,
                self.game_state.card_on_top,
                self.game_state.direction,
                self.game_state.turns_to_stop,
                self.game_state.cards_to_take
            )
            bot.set_bot_data(data_for_bot)

    cpdef update_ai(self, bot):
        if isinstance(bot, BaseAIBot.BaseAIBot):
            bot_features = bot.extract_features(self.game_state)
            game_features = self.upgrade_features(data_for_bot=True)
            result = {**bot_features, **game_features}
            bot.create_row(result)

    cpdef manage_player_move(self, player, forced_first_move=None):
        cdef int i
        self.update_bot(player)
        self.update_ai(player)

        if self.show_game:
            self.game_state.show_state(player)

        player_features = player.extract_features(self.game_state)
        if forced_first_move is not None:
            player.show_hand()
            card_played = forced_first_move
        else:
            card_played = player.move(first_card_taken=forced_first_move, game=self)

        if card_played.match(self.game_state.card_on_top):
            if self.game_state.turns_to_stop != 0:
                if not self.manage_stop(player, card_played):
                    self.manage_player_move(player)
            elif self.game_state.cards_to_take != 0 and self.is_valid_plus_card(card_played):
                player.play_card(card_played)
                self.game_state.put_card(card_played.play(self.game_state))
            elif (
                self.game_state.cards_to_take != 0 and
                not self.is_valid_plus_card(card_played) and
                not isinstance(card_played, DrawCard)
            ):
                self.manage_player_move(player)
            elif isinstance(card_played, DrawCard):
                if len(self.game_state.deck.deck) <= 1:
                    self.game_state.move_pile_to_deck()
                self.manage_draw(player)
            else:
                player.play_card(card_played)
                self.game_state.put_card(card_played.play(self.game_state))
        else:
            return self.manage_player_move(player)

        if player.get_count_cards_in_hand() == 0:
            self.game_state.set_game_over()

        player_features = self.upgrade_features(player_features, card_played)
        self.game_state.features_list.append(player_features)

        if self.show_game:
            self.game_state.show_card_played(card_played)

        return

    cpdef dict upgrade_features(self, features=None, move=None, bint data_for_bot=False):
        if features is None:
            features = {}
        features["is_game_over"] = self.game_state.get_game_over()
        features["index_of_a_player"] = self.game_state.index_of_a_player
        if not data_for_bot:
            features["game_id"] = self.game_state.game_id
            features["card_played"] = move
        return features

    cpdef list play(self, forced_first_move=None):
        """Main game method. Controls game flow"""
        if (forced_first_move is not None) and self.show_game:
            print(f"Forced move: {forced_first_move.rich_str()}")

        while len(self.game_state.players) > 1:
            self.game_state.check_number_of_cards_in_game()
            self.game_state.round += 1
            player = self.game_state.get_player()

            if self.game_state.round > 1000 and isinstance(player, BaseAIBot.BaseAIBot):
                self.game_state.show_infinite_mistakes()
                break

            if player.stopped:
                player.update_stop_status()
            else:
                self.manage_player_move(player, forced_first_move)
                forced_first_move = None

            if player.has_won():
                self.game_state.drop_player(player, did_not_surrender=True)

            if "Color" in str(self.game_state.card_on_top) and len(self.game_state.pile) > 1:
                raise ValueError("Color on top")

            self.game_state.index_of_a_player = self.game_state.update_player_index()

        self.game_state.drop_player(self.game_state.players[0], did_not_surrender=True)
        self.game_state.reset_all_bots()

        if self.show_game:
            self.game_state.show_game_over()

        return [self.game_state.get_features_list(), self.game_state.ranking_table[0]]
