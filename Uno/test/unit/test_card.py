import pytest
from unittest.mock import MagicMock
from Uno.game.Card import Card, Plus4Card, ColorCard, ReverseCard, StopCard, Plus2Card, DrawCard, SurrenderCard
from Uno.game.Deck import Deck


@pytest.mark.parametrize("c1, c2, expected_result", [
    (Card("0", "Red"), Card("0", "Red"), True),
    (Card("0", "Red"), Card("0", "Blue"), True),
    (Card("0", "Red"), Card("1", "Green"), False),
    (Card("0", "Red"), Card("9", "Yellow"), False),
    (Card("0", "Red"), Plus4Card("+4", "Colors"), True),
    (Card("0", "Red"), ColorCard("All", "Colors"), True),
    (Card("0", "Red"), ReverseCard("Reverse", "Red"), True),
    (Card("0", "Red"), StopCard("Stop", "Red"), True),
    (Card("0", "Red"), Plus2Card("+2", "Red"), True),
    (Card("0", "Red"), DrawCard(), False),
    (Card("0", "Red"), SurrenderCard(), False)
])
def test_match_logic(c1, c2, expected_result):
    assert  c1.match(c2) is expected_result

@pytest.mark.parametrize("c1, c2, expected_result", [
    (Card("0", "Red"), Card("0", "Red"), True),
    (Card("0", "Red"), Card("0", "Blue"), False),
    (Card("0", "Red"), Card("1", "Green"), False),
    (Card("0", "Red"), Card("9", "Yellow"), False),
    (Plus4Card("+4", "Colors"), Plus4Card("+4", "Colors"), True),
    (ColorCard("All", "Colors"), ColorCard("All", "Colors"), True),
    (ColorCard("All", "Colors"), Plus4Card("+4", "Colors"), False),
    (ReverseCard("Reverse", "Red"), ReverseCard("Reverse", "Red"), True),
    (Card("0", "Red"), ReverseCard("Reverse", "Red"), False),
    (Card("0", "Red"), StopCard("Stop", "Red"), False),
    (Plus2Card("+2", "Red"), Plus2Card("+2", "Red"), True),
    (Card("0", "Red"), Plus2Card("+2", "Red"), False),
    (Card("0", "Red"), DrawCard(), False),
    (Card("0", "Red"), SurrenderCard(), False),
    (Card("0", "Red"), None, False),
    (Card("0", "Red"), "0 Red", False),
    (Card("0", "Red"), 123, False),
    (SurrenderCard(), None, False),
])
def test_card_equality(c1, c2, expected_result):
    assert (c1 == c2) is expected_result


@pytest.mark.parametrize("c, color, expected_result",  [
    (ColorCard("All", "Colors"), "Red", True),
    (ColorCard("All", "Colors"), "Blue", True),
    (ColorCard("All", "Colors"), "Green", True),
    (ColorCard("All", "Colors"), "Yellow", True),
    (Plus4Card("All", "Colors"), "Red", True),
    (Plus4Card("All", "Colors"), "Blue", True),
    (Plus4Card("All", "Colors"), "Green", True),
    (Plus4Card("All", "Colors"), "Yellow", True),
    (ColorCard("All", "Colors"), "Black", False),
    (ColorCard("All", "Colors"), "White", False),
    (ColorCard("All", "Colors"), "Gray", False),
    (ColorCard("All", "Colors"), "Purple", False),
    (ColorCard("All", "Colors"), "", False),
    (ColorCard("All", "Colors"), None, False),
    (Plus4Card("All", "Colors"), "Black", False),
    (Plus4Card("All", "Colors"), "White", False),
    (Plus4Card("All", "Colors"), "Gray", False),
    (Plus4Card("All", "Colors"), "Purple", False),
    (Plus4Card("All", "Colors"), "", False),
    (Plus4Card("All", "Colors"), None, False),
])
def test_change_color(c, color, expected_result):
    assert c.change_color(color) is expected_result

def test_special_cards_always_match():
    card = Card("7", "Blue")
    assert ColorCard().match(card) is True
    assert Plus4Card().match(card) is True
    assert DrawCard().match(card) is True
    assert SurrenderCard().match(card) is True

def test_card_str_representation():
    assert str(Card("5", "Red")) == "5 Red"
    assert str(DrawCard()) == "Draw"
    assert str(SurrenderCard()) == "Surrender"

def test_action_cards_play_effects():
    game = MagicMock()
    # Plus2 adds 2 cards to cards_to_take
    Plus2Card("+2", "Red").play(game)
    game.add_cards_to_take.assert_called_with(2)
    # Plus4 adds 4 cards to cards_to_take
    Plus4Card("+4", "Colors").play(game)
    game.add_cards_to_take.assert_called_with(4)
    # Reverse changes the game direction
    ReverseCard("Reverse", "Red").play(game)
    game.change_game_direction.assert_called_once()
    # Stop adds a turn to stop
    StopCard("Stop", "Red").play(game)
    game.add_turns_to_stop.assert_called_once()
    # Surrender card drops a player from the game
    SurrenderCard().play(game)
    game.drop_player.assert_called_once()
    