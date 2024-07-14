import random
from Uno.players.Bot import Bot
from Uno.game.Card import *


class AgressiveBot(Bot):
    def __init__(self, name: str):
        """Initializes bot"""
        super().__init__(name)

    def __str__(self):
        return f":robot:[cyan]BLB {self.name}[/]"

    @staticmethod
    def colors_of_list(list):
        return [card.color for card in list]

    def choose_color(self) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        possible_colors = ["Red", "Green", "Blue", "Yellow"]
        all_colors = self.colors_of_list(self.pile)
        hand_colors = self.colors_of_list(self.hand)
        max_num = 0
        color_to_return = ""
        for color in possible_colors:
            num_of_color = all_colors.count(color)/len(all_colors) + hand_colors.count(color)/len(hand_colors)
            max_num = num_of_color if max_num < num_of_color else max_num
            if color in hand_colors and num_of_color == max_num:
                color_to_return = color
        return color_to_return

        # return random.choice(possible_colors)

    def valid_cards(self) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        valid_cards_to_put = []
        for card in self.hand:
            if card.match(self.card_on_top):
                valid_cards_to_put.append(card)
        if len(valid_cards_to_put) > 0:
            return valid_cards_to_put
        else:
            return []

    def change_color(self, card: ColorCard):
        card.change_color(random.choice(["Red", "Green", "Blue", "Yellow"]))

    def move(self, first_card_taken=None):
        """Handles a different situations of game state and reacts accordingly"""
        # If bot could be stopped it plays stop card
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

        # If there are no unusual states it picks random card from those possible to play
        else:
            if len(self.valid_cards()) > 0:
                choosen_card = random.choice(self.valid_cards())
                if isinstance(choosen_card, ColorCard):
                    self.change_color(choosen_card)
                return choosen_card
            else:
                return DrawCard()
