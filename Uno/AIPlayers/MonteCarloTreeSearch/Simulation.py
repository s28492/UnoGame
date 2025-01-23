#!/usr/bin/env python
import copy
import random

from Uno.players.Bot import Bot
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.AIPlayers.MonteCarloTreeSearch.Node import Node
from Uno.game.Card import Card, Plus4Card, DrawCard, ColorCard, StopCard
from Uno.game.Game import Game
from Uno.game.GameState import GameState
from Uno.game.Deck import Deck
from Uno.players.AgressiveBot import AgressiveBot
from Uno.players.RandomBot import BotRandom
from Uno.AIPlayers.MonteCarloTreeSearch.game.CGameSimulation import GameSimulation
# from Uno.AIPlayers.MonteCarloTreeSearch.game.GameSimulation import GameSimulation

class Simulation:
    """
    Manages the game logic and interactions with GameState.
    """

    def __init__(self, game: Game, mcts_bot_hand: list[Card], action: Card):
        self.game = game
        self.mcts_bot_hand = mcts_bot_hand
        self.player_1: Bot = AgressiveBot("MCTSBot")
        # self.player_1: Bot = ID3Bot("MCTSBot", "Uno/DecisionTrees/LightModels/20241230_1324_LIGHT_20241227_1251_3GB_Dataset_with_child_map.pkl")
        self.player_2: Bot = AgressiveBot("EnemyBot")
        self.new_game = GameSimulation([self.player_1, self.player_2], show_game=False)
        self.new_game_state = GameState([self.player_1, self.player_2], is_simulation=True)
        self.action = copy.deepcopy(action)
        self.deck = Deck()

    def __recreate_game_state(self):
        # Setting up all basic elements of GameState
        self.new_game_state.set_move_history(copy.deepcopy(self.game.get_game_state().move_history))
        # Do not set up round because we want our bot to start
        # self.new_game_state.set_round(copy.deepcopy(self.game.get_game_state().round))
        self.new_game_state.set_deck(self.deck)
        self.new_game_state.set_pile(self.copy_card_list(self.game.get_game_state().get_pile()))
        self.new_game_state.set_reset_colors(copy.deepcopy(self.game.get_game_state().get_reset_colors()))
        self.new_game_state.set_card_on_top(copy.deepcopy(self.game.get_game_state().get_card_on_top()))
        # Do not set up index_of_a_player, because we want to our bot to start
        # self.new_game_state.set_index_of_a_player(copy.deepcopy(self.game.get_game_state().index_of_a_player))
        self.new_game_state.set_direction(copy.deepcopy(self.game.get_game_state().get_direction()))
        self.new_game_state.set_turns_to_stop(copy.deepcopy(self.game.get_game_state().get_turns_to_stop()))
        self.new_game_state.set_cards_to_take(copy.deepcopy(self.game.get_game_state().get_cards_to_take()))
        self.new_game_state.set_first_taken(copy.deepcopy(self.game.get_game_state().get_first_taken()))
        self.new_game_state.set_features_list(copy.deepcopy(self.game.get_game_state().get_features_list()))
        # Assign new_game_state to new_game
        self.new_game.set_game_state(self.new_game_state)

    def set_bot_status(self):
        self.player_1.set_bot_turns_to_stop(self.new_game_state.get_turns_to_stop())
        self.player_1.set_bot_cards_to_take(self.new_game_state.get_cards_to_take())

    def copy_card_list(self, card_list: list[Card]):
        new_card_list = []
        for card in card_list:
            new_card_list.append(copy.deepcopy(card))
        return new_card_list

    def initialize_game(self) -> None:
        """Initializes a game"""
        self.__deal_cards()
        self.__recreate_game_state()
        self.set_bot_status()

    def __deal_cards(self):
        all_visible_cards = self.mcts_bot_hand + self.game.get_game_state().get_pile()
        all_visible_cards = self.copy_card_list(all_visible_cards)
        # Removing visible cards from deck
        for card in all_visible_cards:
            success: bool = self.deck.remove_card_from_deck(card)
            if not success:
                print()
                for deck_card in self.deck.get_deck():
                    print(deck_card, end=" ")
                print(f"\n\n {card}")
                raise ValueError(f"Card not found in deck: {card}")
        number_of_cards_in_enemy_hand = 108 - (len(all_visible_cards) + self.game.get_game_state().get_num_cards_left_in_deck())
        enemy_hand = []
        # Setting enemy and deck cards
        for i in range(number_of_cards_in_enemy_hand):
            card = random.choice(self.deck.get_deck())
            enemy_hand.append(card)
            self.deck.get_deck().remove(card)

        self.player_2.set_hand(enemy_hand)
        self.player_1.set_hand(self.copy_card_list(self.mcts_bot_hand))

    def get_deck(self):
        return self.deck

    def play(self):
        return 0 if self.new_game.play(forced_first_move=self.action)[1].get_name() == "EnemyBot" else 1