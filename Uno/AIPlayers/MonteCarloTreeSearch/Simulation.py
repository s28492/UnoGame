#!/usr/bin/env python
import random

from Uno.players.Bot import Bot
from Uno.AIPlayers.BaseAIBot import BaseAIBot
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.AIPlayers.MonteCarloTreeSearch.Node import Node
from Uno.game.Card import Card, Plus4Card, DrawCard, ColorCard, StopCard, SurrenderCard
from Uno.game.Game import Game
from Uno.game.GameState import GameState
from Uno.game.Deck import Deck
from Uno.players.AgressiveBot import AgressiveBot
from Uno.players.BasicLogicBot import BasicLogicBot
from Uno.players.RandomBot import BotRandom
# from Uno.AIPlayers.MonteCarloTreeSearch.game.CGameSimulation import GameSimulation
from Uno.AIPlayers.MonteCarloTreeSearch.game.GameSimulation import GameSimulation

class Simulation:
    """
    Manages the game logic and interactions with GameState.
    """

    def __init__(self, game: Game, mcts_bot_hand: list[Card], action: Card):
        self.__game = game
        self.__mcts_bot_hand = mcts_bot_hand
        self.__player_1_instance: Bot = BasicLogicBot("MCTSBot") 
        self.__player_2_instance: Bot = BasicLogicBot("EnemyBot") 
        self.__new_game = GameSimulation([self.__player_1_instance, self.__player_2_instance], show_game=False)
        self.__new_game_state = GameState([self.__player_1_instance, self.__player_2_instance], is_simulation=True)
        self.__action = self.__copy_card(action)
        self.__deck = Deck()

    def __recreate_game_state(self):
        # Setting up all basic elements of GameState
        # The  round is not set because MCTS bot has to go first
        # self.new_game_state.set_round(copy.deepcopy(self.game.get_game_state().round))
        self.__new_game_state.set_deck(self.__deck)
        self.__new_game_state.set_pile(self.__copy_card_list(self.__game.get_game_state().get_pile()))
        self.__new_game_state.set_card_on_top(self.__copy_card(self.__game.get_game_state().get_card_on_top()))
        # The index_of_a_player is not set up, because MCTS bot has go first
        # self.new_game_state.set_index_of_a_player(copy.deepcopy(self.game.get_game_state().index_of_a_player))
        self.__new_game_state.set_direction(self.__game.get_game_state().get_direction())
        self.__new_game_state.set_turns_to_stop(self.__game.get_game_state().get_turns_to_stop())
        self.__new_game_state.set_cards_to_take(self.__game.get_game_state().get_cards_to_take())
        self.__new_game_state.set_first_taken(self.__copy_card(self.__game.get_game_state().get_first_taken()))
        # Assign new_game_state to new_game
        self.__new_game.set_game_state(self.__new_game_state)

    def __set_bot_status(self):
        self.__player_1_instance.set_bot_turns_to_stop(self.__new_game_state.get_turns_to_stop())
        self.__player_1_instance.set_bot_cards_to_take(self.__new_game_state.get_cards_to_take())
        
    def __copy_card(self, card):
        if card is None or isinstance(card, bool):
            return card
        if isinstance(card, (DrawCard, SurrenderCard)):
            return type(card)()
        new_card = type(card)(card.value, card.color)
        new_card.color = card.color
        new_card.value = card.value
        return new_card

    def __copy_card_list(self, card_list: list[Card]):
        return [self.__copy_card(card) for card in card_list]

    def initialize_game(self) -> None:
        """Initializes a game"""
        self.__deal_cards()
        self.__recreate_game_state()
        self.__set_bot_status()

    def __deal_cards(self):
        all_visible_cards = self.__mcts_bot_hand + self.__game.get_game_state().get_pile()
        all_visible_cards = self.__copy_card_list(all_visible_cards)
        # Removing visible cards from deck
        for card in all_visible_cards:
            success: bool = self.__deck.remove_card_from_deck(card)
            if not success:
                print()
                for deck_card in self.__deck.get_deck():
                    print(deck_card, end=" ")
                print(f"\n\n {card}")
                raise ValueError(f"Card not found in deck: {card}")
        number_of_cards_in_enemy_hand = 108 - (len(all_visible_cards) + self.__game.get_game_state().get_num_cards_left_in_deck())
        enemy_hand = []
        # Setting enemy and deck cards
        for i in range(number_of_cards_in_enemy_hand):
            card = random.choice(self.__deck.get_deck())
            enemy_hand.append(card)
            self.__deck.get_deck().remove(card)

        self.__player_2_instance.set_hand(enemy_hand)
        self.__player_1_instance.set_hand(self.__copy_card_list(self.__mcts_bot_hand))

    def get_deck(self):
        return self.__deck

    def play(self):
        return 0 if self.__new_game.play(forced_first_move=self.__action)[1].get_name() == "EnemyBot" else 1