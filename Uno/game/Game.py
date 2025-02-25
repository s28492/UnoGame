from Uno.players.Bot import Bot
from Uno.AIPlayers import BaseAIBot
from Uno.game.Card import Card, Plus4Card, DrawCard, ColorCard
from Uno.game.GameState import GameState
class Game:
    """
    Manages the game logic and interactions with GameState.
    """

    def __init__(self, players: list, has_human_player=False):
        self.__has_human_player = has_human_player
        self.__game_state = GameState(players)
        self._initialize_game()

    def _initialize_game(self) -> None:
        """Initializes a game"""
        self.__game_state.put_card(self.__game_state.deck.draw_card())

    def get_game_state(self):
        return self.__game_state

    def _manage_stop(self, player, card):
        """
        Handles the logic of stop card and updating turns to stop variable.
        """
        if card.value == "Stop" and card.color == "Stop":
            if self.__game_state.turns_to_stop == 1:
               self.__game_state.turns_to_stop = 0
               return True
            else:
                player.stop_player(self.__game_state.turns_to_stop - 1)
                self.__game_state.turns_to_stop = 0
                return True
        elif card.value == "Stop":
            self.__game_state.add_turns_to_stop()
            player.play_card(card)
            self.__game_state.put_card(card)
            return True
        return False
    def _manage_draw(self, player, first_card_taken = None):
        if first_card_taken is None:
            first_card_taken = self.__game_state.take_card(player)
            self.__game_state.cards_to_take = self.__game_state.cards_to_take - 1 if self.__game_state.cards_to_take != 0 else 0

        if self.__game_state.cards_to_take != 0 and self._is_valid_plus_card(first_card_taken):
            if not isinstance(self.__game_state.get_player(), Bot):
                self.__game_state.console.print(
                 f"You have drawed {first_card_taken.rich_str()}. Do you want to put it? Write \"Draw\" if you want to take rest of the cards.")
            player_move = player.move(first_card_taken, game=self)
            if isinstance(player_move, DrawCard):
                for i in range(self.__game_state.cards_to_take):
                    self.__game_state.take_card(player)
                self.__game_state.cards_to_take = 0
            elif player_move.match(self.__game_state.card_on_top) and player_move == first_card_taken or (isinstance(first_card_taken, ColorCard) and first_card_taken.value == player_move.value):
                player.play_card(player_move)
                self.__game_state.put_card(player_move.play(self.__game_state))
            else:
                self._manage_draw(player, first_card_taken=first_card_taken)
        elif self.__game_state.cards_to_take == 0 and first_card_taken is not None and first_card_taken.match(self.__game_state.card_on_top):
            if not isinstance(self.__game_state.get_player(), Bot):
                self.__game_state.console.print(
                 f"You have drawed {first_card_taken.rich_str()}. Do you want to put it? Write \"Draw\" if you want to keep it and take {self.__game_state.cards_to_take} remaining cards")
            player_move = player.move(first_card_taken, game=self)
            if player_move == first_card_taken or (isinstance(first_card_taken, ColorCard) and first_card_taken.value == player_move.value):
                player.play_card(player_move)
                self.__game_state.put_card(player_move.play(self.__game_state))
            elif isinstance(player_move, DrawCard):
                return
            else:
                if not isinstance(self.__game_state.get_player(), Bot):
                    self.__game_state.console.print(
                     "You have to choose the card you have drawed or just write \"Draw\" if you want to keep it.")
                self._manage_draw(player, first_card_taken=first_card_taken)
        else:
            for i in range(self.__game_state.cards_to_take):
                self.__game_state.take_card(player)
            self.__game_state.cards_to_take = 0
    def _is_valid_plus_card(self, card):
        if card.__class__ == self.__game_state.card_on_top.__class__ or isinstance(card, Plus4Card):
            return True
        return False

    def _update_bot(self, bot):
        if isinstance(bot, Bot):
            data_for_bot = (self.__game_state.get_players(), self.__game_state.pile, self.__game_state.card_on_top
                            , self.__game_state.direction, self.__game_state.turns_to_stop, self.__game_state.cards_to_take)
            bot.set_bot_data(data_for_bot)
            # bot.set_game_state(self.__game_state)

    def update_ai(self, bot):
        if isinstance(bot, BaseAIBot.BaseAIBot):
            bot_features = bot.extract_features(self.__game_state)
            game_features = self._upgrade_features(data_for_bot=True)
            result = {**bot_features, **game_features}
            bot.create_row(result)

    def _manage_player_move(self, player):
        self._update_bot(player)
        self.update_ai(player)
        if not isinstance(player, Bot):
           self.__game_state.show_state(player)
        player_features = player.extract_features(self.__game_state)
        card_played = player.move(game=self)
        if card_played.match(self.__game_state.card_on_top):
            if self.__game_state.turns_to_stop != 0:
                if not self._manage_stop(player, card_played):
                    self._manage_player_move(player)
            elif self.__game_state.cards_to_take != 0 and self._is_valid_plus_card(card_played):
                player.play_card(card_played)
                self.__game_state.put_card(card_played.play(self.__game_state))
            elif self.__game_state.cards_to_take != 0 and not self._is_valid_plus_card(card_played) and not isinstance(card_played, DrawCard):
               self._manage_player_move(player)
            elif isinstance(card_played, DrawCard):
                if len(self.__game_state.deck.deck) <= 1:
                   self.__game_state.move_pile_to_deck()
                self._manage_draw(player)
            else:
                player.play_card(card_played)
                self.__game_state.put_card(card_played.play(self.__game_state))
        else:
            return self._manage_player_move(player)

        if player.get_count_cards_in_hand() == 0:
             self.__game_state.set_game_over()
        player_features = self._upgrade_features(player_features, card_played)
        self.__game_state.features_list.append(player_features)

    def _upgrade_features(self, features = None, move = None, data_for_bot = False):
        if features is None:
            features = {}
        features["is_game_over"] = self.__game_state.get_game_over()
        features["index_of_a_player"] = self.__game_state.index_of_a_player
        if not data_for_bot:
           features["game_id"] = self.__game_state.game_id
           features["card_played"] = move
        return features

    def play(self) -> list:
        """Main game method. Controls game flow"""
        while len(self.__game_state.players) > 1:
            self.__game_state.check_number_of_cards_in_game()
            self.__game_state.round += 1
            player = self.__game_state.get_player()
            if self.__game_state.round > 1_000 and isinstance(player, BaseAIBot.BaseAIBot):
                 self.__game_state.show_infinite_mistakes()
                 break
            # Checks if player is stopped
            if player.stopped:
                player.update_stop_status()
            else:
                self._manage_player_move(player)
            if player.has_won():
               self.__game_state.drop_player(player, did_not_surrender=True)

            if "Color" in str(self.__game_state.card_on_top) and len(self.__game_state.pile) > 1:
                raise ValueError("Color on top")

            self.__game_state.index_of_a_player = self.__game_state.update_player_index()

        self.__game_state.drop_player(self.__game_state.players[0], did_not_surrender=True)

        self.__game_state.reset_all_bots()
        return [self.__game_state.get_features_list(), self.__game_state.ranking_table[0]]