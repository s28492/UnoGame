import random
from Uno.players.Bot import Bot
from Uno.game.Card import *


class BLBUpgradedColorChoosing(Bot):
    card_in_game_dict = {"<class 'Uno.game.Card.Card'>": 76
        , "<class 'Uno.game.Card.ReverseCard'>": 8
        , "<class 'Uno.game.Card.StopCard'>": 8
        , "<class 'Uno.game.Card.Plus2Card'>": 8
        , "<class 'Uno.game.Card.Plus4Card'>": 4
        , "<class 'Uno.game.Card.ColorCard'>": 4}
    def __init__(self, name: str= ""):
        """Initializes bot"""
        super().__init__(name)
        self.card_in_game_dict_instance = None
        print("Bye")

    def __str__(self):
        return f":robot:[cyan]BLB {self.name}[/]"

    @staticmethod
    def colors_of_list(list):
        return [card.color for card in list]

    @staticmethod
    def card_of_given_color_from_list(color, list_of_cards):
        for card in list_of_cards:
            if card.color == color:
                return card

    def choose_color(self, card_of_given_type=None) -> str:
        """Bot chooses color of "Color" card based on what color he has the most in "hand\""""
        cards = ""
        for card in card_of_given_type:
            cards += f"{card} "
        all_colors = self.colors_of_list(self.pile)
        hand_colors = self.colors_of_list(self.hand)
        max_num = 0
        color_to_return = ""
        for color in self.possible_colors:
            if color not in self.colors_of_list(card_of_given_type):
                continue
            num_of_color = all_colors.count(color) / len(all_colors) + hand_colors.count(color) / len(hand_colors)
            max_num = num_of_color if max_num < num_of_color else max_num
            if color in hand_colors and card_of_given_type is None and num_of_color == max_num:
                color_to_return = color
            elif card_of_given_type is not None and num_of_color == max_num:
                color_to_return = color
        return color_to_return

        # return random.choice(possible_colors)

    def change_color(self, card: ColorCard):
        card.change_color(random.choice(["Red", "Green", "Blue", "Yellow"]))

    def move(self, first_card_taken=None, game=None):
        """Handles a different situations of game state and reacts accordingly"""
        # If bot could be stopped it plays stop card
        if isinstance(first_card_taken, ColorCard):
            self.change_color(first_card_taken)

        if first_card_taken is not None:
            return first_card_taken

        if self.turns_to_stop > 0:
            if len(self.stop_cards) == 0:
                return StopCard("Stop", "Stop")
            color = self.choose_color(self.stop_cards)
            card_to_play = self.card_of_given_color_from_list(color, self.stop_cards)
            return card_to_play
        # If Plus2Card was played it reacts with Plus2Cards or Plus4Cards card
        elif self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            if len(self.plus_2_cards) + len(self.plus_4_cards) == 0:
                return DrawCard()
            if len(self.plus_2_cards) > 0:
                color = self.choose_color(self.plus_2_cards)
                card_to_play = self.card_of_given_color_from_list(color, self.plus_2_cards)
                return card_to_play

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
            if len(self.valid_cards(first_card_taken)) > 0:
                choosen_card = random.choice(self.valid_cards(first_card_taken))
                if isinstance(choosen_card, ColorCard):
                    self.change_color(choosen_card)
                return choosen_card
            else:
                return DrawCard()
