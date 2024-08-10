import random
from Uno.game.Card import *
from Uno.players.Bot import Bot


class BotRandom(Bot):
    def __init__(self, name: str = ""):
        """Initializes bot"""
        super().__init__(name)


    def __str__(self):
        return f":robot:[cyan] Random Bot {self.name}[/]"


    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        return random.choice(possible_colors)

    def valid_cards(self, card_taken = None) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards_plus_2 = self.collect_valid_cards_of_given_instance(Plus2Card)
            valid_cards_plus_4 = self.collect_valid_cards_of_given_instance(Plus4Card)
            if len(valid_cards_plus_2) > 0:
                return valid_cards_plus_2
            elif len(valid_cards_plus_4) > 0:
                return valid_cards_plus_4
            else:
                return [DrawCard()]

        valid_cards = self.collect_valid_cards_of_given_instance(Card)

        return valid_cards if len(valid_cards) > 0 else [DrawCard()]


    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                valid_cards_to_put.append(card)
        return valid_cards_to_put


    def change_color(self, card: ColorCard):
        card.change_color(self.choose_color())

    def move(self, first_card_taken=None):
        """Handles a different situations of game state and reacts accordingly"""
        if isinstance(first_card_taken, ColorCard):
            self.change_color(first_card_taken)

        if first_card_taken is not None:
            return first_card_taken

        valid_cards = self.valid_cards()
        card_to_play = random.choice(valid_cards)
        if isinstance(card_to_play, ColorCard):
            self.change_color(card_to_play)
        return card_to_play
