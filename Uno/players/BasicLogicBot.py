import random
from Uno.players.Bot import Bot
from Uno.game.Card import *


class BasicLogicBot(Bot):
    def __init__(self, name: str= ""):
        """Initializes bot"""
        super().__init__(name)

    def __str__(self):
        return f":robot:[cyan]BLB {self.name}[/]"


    def change_color(self, card: ColorCard):
        card.change_color(self.choose_color())

    def collect_valid_basic_cards(self):
        '''returns basic cards that can be played'''
        valid_cards_to_put = []

        for card in self.hand:
            if card.match(self.card_on_top):
                if not isinstance(card, ColorCard) and not isinstance(card, StopCard) and not isinstance(card, Plus2Card) and not isinstance(card, ReverseCard):
                    valid_cards_to_put.append(card)
        return valid_cards_to_put
    
    def collect_valid_special_cards(self):
        '''returns special cards that can be played'''
        valid_cards_to_put = []

        for card in self.hand:
            if card.match(self.card_on_top):
                if isinstance(card, ColorCard) or isinstance(card, StopCard) or isinstance(card, Plus2Card) or isinstance(card, ReverseCard):
                    valid_cards_to_put.append(card)
        return valid_cards_to_put

    def valid_basic_cards(self, card_taken=None) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        valid_cards = []
        if card_taken is not None:
            return []

        if self.turns_to_stop != 0:
            return []

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            return []

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            return []

        valid_cards = self.collect_valid_basic_cards()

        return valid_cards

    def move(self, first_card_taken = None, game=None):
        """Handles a different situations of game state and reacts accordingly"""
        if isinstance(first_card_taken, ColorCard):
            self.change_color(first_card_taken)

        if first_card_taken is not None:
            return first_card_taken

        if self.turns_to_stop > 0:
            if len(self.stop_cards) == 0:
                return StopCard("Stop", "Stop")
            return random.choice(self.stop_cards)
            
        # If Plus2Card was played it reacts with Plus2Cards or Plus4Cards card
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            if len(self.plus_2_cards) + len(self.plus_4_cards) == 0:
                return DrawCard()
            if len(self.plus_2_cards) > 0:
                return random.choice(self.plus_2_cards)

            if len(self.plus_4_cards) > 0:
                choosen_card = random.choice(self.plus_4_cards)
                self.change_color(choosen_card)
                return choosen_card

        # if Plus4Cards was played it reacts with Plus4Card card
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            if len(self.plus_4_cards) == 0:
                return DrawCard()
            plus_card = random.choice(self.plus_4_cards)
            self.change_color(plus_card)
            return plus_card

        else:
            basic_cards = self.collect_valid_basic_cards()
            special_cards = self.collect_valid_special_cards()
            opponent = [p for p in self.players if p != self][0]

            # 1. If opponent has <= 2 cards, attack him with a special card:
            if len(opponent.hand) <= 2 and len(special_cards) > 0:
                choosen_card = random.choice(special_cards)
                if isinstance(choosen_card, ColorCard):
                    self.change_color(choosen_card)
                return choosen_card
            # 2. In normal situation, play a normal card:
            if len(basic_cards) > 0:
                return random.choice(basic_cards)
            # 3. No normal cards, play a special card:
            if len(special_cards) > 0:
                choosen_card = random.choice(special_cards)
                if isinstance(choosen_card, ColorCard):
                    self.change_color(choosen_card)
                return choosen_card
            # 4. No cards at all, draw a card:
            return DrawCard()
