from Uno.players.Bot import Bot
from Uno.game.Deck import Deck
from Uno.game.Game import Game
import pytest

@pytest.fixture(scope="class")
def deck_instance():
    deck_obj = Deck()
    Deck.create_deck(deck_obj)
    return deck_obj

@pytest.fixture(scope="class")
def player_instance():
    player1 = Bot("One")
    player2 = Bot("Two")
    return [player1, player2]
@pytest.fixture(scope="class")
def game_instance(deck_instance, player_instance):
    game = Game(player_instance)
    game.deck = deck_instance
    game.deal_cards_to_players()
    game.pile = game.deck.deck[:len(game.deck.deck) // 2]
    game.deck.deck = game.deck.deck[len(game.deck.deck) // 2:]
    return game
