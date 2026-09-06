import pytest
from Uno.game.Deck import Deck
from Uno.game.Card import Card, DrawCard, ReverseCard, Plus2Card, Plus4Card, ColorCard, StopCard, SurrenderCard

@pytest.fixture
def deck_instance()-> Deck:
    """Returns initialized deck instance"""
    deck = Deck()
    return deck

@pytest.fixture
def empty_deck() -> Deck:
    """Returns empty deck instance"""
    deck = Deck()
    deck.set_deck([])
    return deck


@pytest.fixture
def sample_valid_cards() -> list[Card]:
    """Zwraca listę zawierającą reprezentację każdego typu karty dziedziczącej po Card."""
    return [
        Card("5", "Red"),
        ReverseCard("Reverse", "Blue"),
        StopCard("Stop", "Green"),
        Plus2Card("+2", "Yellow"),
        Plus4Card("+4", "Colors"),
        ColorCard("All", "Colors"),
        ColorCard("All", "Red"),
        ColorCard("All", "Green"),
        ColorCard("All", "Blue"),
        ColorCard("All", "Yellow"),
        Plus4Card("+4", "Colors"),
        Plus4Card("+4", "Red"),
        Plus4Card("+4", "Green"),
        Plus4Card("+4", "Blue"),
        Plus4Card("+4", "Yellow"),
        Plus2Card("+2", "Colors"),
        Plus2Card("+2", "Red"),
        Plus2Card("+2", "Green"),
        Plus2Card("+2", "Blue"),
        Plus2Card("+2", "Yellow"),
        ReverseCard("Reverse", "Red"),
        ReverseCard("Reverse", "Green"),
        ReverseCard("Reverse", "Blue"),
        ReverseCard("Reverse", "Yellow"),
        StopCard("Stop", "Red"),
        StopCard("Stop", "Green"),
        StopCard("Stop", "Blue"),
        StopCard("Stop", "Yellow"),
    ]

def test_new_deck_has_all_cards(deck_instance):
    cards = deck_instance.get_all_cards()
    
    assert deck_instance.deck_length() == 108
    assert len([c for c in cards if isinstance(c, ReverseCard)]) == 8
    assert len([c for c in cards if isinstance(c, StopCard)]) == 8
    assert len([c for c in cards if isinstance(c, Plus2Card)]) == 8
    assert len([c for c in cards if isinstance(c, Plus4Card)]) == 4
    assert len([c for c in cards if isinstance(c, ColorCard)]) == 8 #4 Wild and 4 Plus4 cards

def test_new_deck_has_all_colors(deck_instance):
    cards = deck_instance.get_all_cards()

    assert len([c for c in cards if c.color == "Red"]) == 25
    assert len([c for c in cards if c.color == "Yellow"]) == 25
    assert len([c for c in cards if c.color == "Green"]) == 25
    assert len([c for c in cards if c.color == "Blue"]) == 25
    assert len([c for c in cards if c.color == "Colors"]) == 8

def test_deck_is_shuffled_properly(deck_instance):
    deck_instance.shuffle_deck()
    assert deck_instance.deck_length() == 108

def test_draw_card_removes_card_from_deck(deck_instance):
    deck_instance.draw_card()
    assert deck_instance.deck_length() == 107

def test_multiple_draws(deck_instance):
    for i in range(107):
        deck_instance.draw_card()
        assert deck_instance.deck_length() == 107 - i

@pytest.mark.parametrize("invalid_cards", [
    ["Invalid Card"],
    [[Card("7", "Blue"), DrawCard()]],
    [DrawCard(), Card("7", "Blue"), Plus2Card("7", "Blue"), Deck()],
    [[]],
    [None]
])
def test_cards_to_deck_raises_error_for_invalid_card_type(deck_instance, invalid_cards):
    with pytest.raises(AssertionError):
        deck_instance.cards_to_deck(invalid_cards)

@pytest.mark.parametrize("initial_deck_size, cards_to_add", [
    (108, 1),    
    (108, 108),  
    (100, 9),    
    (54, 55),    
    (1, 108),    
    (0, 109),    
    (0, 200),    
])
def test_cards_to_deck_raises_error_for_invalid_amount_of_cards(
    empty_deck, initial_deck_size, cards_to_add
    ):
    empty_deck.set_deck([Card("7", "Blue")] * initial_deck_size)
    cards = [Card("7", "Blue")] * cards_to_add

    with pytest.raises(AssertionError) as exc_info:
        empty_deck.cards_to_deck(cards)

@pytest.mark.parametrize("invalid_deck", [
    {},
    (),
    Deck(),
    True,
    False,
    None,
    "Invalid Deck"
])
def test_set_deck_raises_error_for_invalid_deck_type(deck_instance, invalid_deck):
    with pytest.raises(AssertionError):
        deck_instance.set_deck(invalid_deck)

def test_reshuffling_discard_pile(empty_deck, sample_valid_cards):
    empty_deck.reshuffle_discard_pile(sample_valid_cards)
    number_of_wild_cards_in_test = len([c for c in sample_valid_cards if isinstance(c, ColorCard)])
    number_of_wild_colors_in_test = len([c for c in sample_valid_cards if c.value == "All"])
    number_of_plus4_cards_in_test = len([c for c in sample_valid_cards if isinstance(c, Plus4Card)])
    number_of_plus2_cards_in_test = len([c for c in sample_valid_cards if isinstance(c, Plus2Card)])
    number_of_reverse_cards_in_test = len([c for c in sample_valid_cards if isinstance(c, ReverseCard)])
    number_of_stop_cards_in_test = len([c for c in sample_valid_cards if isinstance(c, StopCard)])

    assert empty_deck.deck_length() == len(sample_valid_cards)
    assert len([c for c in empty_deck.deck if isinstance(c, ColorCard)]) == number_of_wild_cards_in_test
    assert len([c for c in empty_deck.deck if c.value == "All"]) == number_of_wild_colors_in_test
    assert len([c for c in empty_deck.deck if c.value == "+4"]) == number_of_plus4_cards_in_test
    assert len([c for c in empty_deck.deck if c.value == "+2"]) == number_of_plus2_cards_in_test
    assert len([c for c in empty_deck.deck if c.value == "Reverse"]) == number_of_reverse_cards_in_test
    assert len([c for c in empty_deck.deck if c.value == "Stop"]) == number_of_stop_cards_in_test

@pytest.mark.parametrize("invalid_discard_pile", [
    {"Invalid Deck"},
    True,
    False,
    None,
    "Invalid Deck",
    10
])
def test_reshuffle_discard_pile_type_exception(empty_deck, invalid_discard_pile):
    with pytest.raises(AssertionError):
        empty_deck.reshuffle_discard_pile(invalid_discard_pile)

@pytest.mark.parametrize("small_deck_instance", [
    (Deck(), ([ColorCard("All", "Colors")] * 10), "Cards in deck:\n| " + "All Colors | " * 10),
    (Deck(), ([ColorCard("All", "Blue")] * 10), "Cards in deck:\n| " + "All Blue | " * 10),
    (Deck(), ([Card("7", "Blue")] * 10), "Cards in deck:\n| " + "7 Blue | " * 10)
])
def test_return_string_of_cards_in_deck(deck_instance, empty_deck, small_deck_instance):
    small_deck_instance[0].set_deck(small_deck_instance[1])

    assert deck_instance.return_string_of_cards_in_deck() != "No cards"
    assert isinstance(deck_instance.return_string_of_cards_in_deck(), str)
    assert empty_deck.return_string_of_cards_in_deck() == "No cards"
    assert small_deck_instance[0].return_string_of_cards_in_deck() == small_deck_instance[2]

def test_return_deck(deck_instance, empty_deck):
    assert isinstance(deck_instance.get_deck(), list)
    assert deck_instance.get_deck() == deck_instance.deck
    assert isinstance(empty_deck.get_deck(), list)
    assert empty_deck.get_deck() == []
    

def test_draw_card(empty_deck, deck_instance):
    assert empty_deck.draw_card() is None
    
    drawn_card = deck_instance.draw_card()
    assert isinstance(drawn_card, Card)
    assert deck_instance.deck_length() == 107
    assert drawn_card in deck_instance.all_cards



def test_cards_to_deck_success(empty_deck, sample_valid_cards):
    empty_deck.cards_to_deck(sample_valid_cards)
    assert empty_deck.deck_length() == len(sample_valid_cards)

def test_remove_card_from_deck(deck_instance):
    assert deck_instance.remove_card_from_deck(Plus4Card()) is True
    assert deck_instance.remove_card_from_deck(ColorCard()) is True
    assert deck_instance.remove_card_from_deck(Card("0", "Red")) is True
    assert deck_instance.remove_card_from_deck(Card("0", "Red")) is False
