import pytest


@pytest.mark.usefixtures('deck_instance', 'deck_instance', 'player_instance')
class TestDeckManagement:
    def test_deck_shuffle(self, deck_instance
                          , player_instance, game_instance):
        game = game_instance
        deck = deck_instance
        players = player_instance
        print(f"Player1 cards num: {len(players[0].hand)}")
        print(f"Player1 cards num: {len(players[1].hand)}")
        print(f"Deck cards num: {deck.deck_length()}")
        print(f"Pile cards num: {len(game.get_pile())}")
        all_cards_num = (len(players[0].hand) + len(players[0].hand)
                         + deck.deck_length() + len(game.get_pile()))
        print(f"All cards num: {all_cards_num}")
        game.move_pile_to_deck()

        all_cards_after = (len(players[0].hand) + len(players[0].hand)
                         + deck.deck_length() + len(game.get_pile()))
        print(f"Player1 cards num: {len(players[0].hand)}")
        print(f"Player1 cards num: {len(players[1].hand)}")
        print(f"Deck cards num: {deck.deck_length()}")
        print(f"Pile cards num: {len(game.get_pile())}")
        print(f"All cards num: {all_cards_num}")
        assert all_cards_num == all_cards_after

    def test_create_deck(self, deck_instance):
        deck = deck_instance.create_deck()
        assert len(deck) == 108
