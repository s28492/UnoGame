from Uno.game.Deck import Deck
from Uno.game.Card import Card, DrawCard, ReverseCard, Plus2Card, Plus4Card, ColorCard, StopCard, SurrenderCard

def test_new_deck_has_108_cards():
    deck = Deck()
    assert deck.deck_length() == 108

def test_deck_is_shuffled_properly():
    deck = Deck()
    deck.shuffle_deck()
    assert deck.deck_length() == 108

def test_draw_card_removes_card_from_deck():
    deck = Deck()
    deck.draw_card()
    assert deck.deck_length() == 107
