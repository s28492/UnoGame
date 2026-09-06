from Uno.game.Card import Card, SurrenderCard, DrawCard, StopCard, ColorCard, Plus4Card, Plus2Card, ReverseCard
from rich.console import Console

console = Console()

class Player:
    def __init__(self, name: str = ""):
        if name == "":
            self.name = type(self)
        else:
            self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0
        self.cards_to_take = 0
        self.first_taken = False
        self.console = console
        self.card_on_top = None
        self.turns_to_stop = 0

        self.possible_colors = ["Red", "Green", "Blue", "Yellow"]
        self.features = {}

    def get_name(self):
        return self.name

    def get_features(self):
        return self.features

    def add_card_to_hand(self, card: Card):
        self.hand.append(card)

    def current_state_to_string(self):
        state_string = ""
        state_string += f"Player: {self.name}\n"
        state_string += f"Hand: "
        for card in self.hand:
            state_string += f"{card} |  "
        state_string += "\n"
        state_string += f"Stop status: {self.stop_status}\n"
        state_string += f"cards to take status: {self.cards_to_take}\n"
        state_string += f"First taken: {self.first_taken}\n"
        for feature in self.features:
            state_string += f"{feature}: {self.features[feature]}\n"
        return state_string

    def count_cards(self):
        card_dict = {
            "Red": 0,
            "Green": 0,
            "Blue": 0,
            "Yellow": 0,
            "Stop": 0,
            "+2": 0,
            "+4": 0,
            "Colors": 0
        }
        for card in self.hand:
            if card.color in card_dict:
                card_dict[card.color] += 1
            if card.value in card_dict:
                card_dict[card.value] += 1
        return card_dict

    def extract_features(self, game):
        card_counts = self.count_cards()
        valid_cards_to_play = self.valid_cards(card_taken=None)
        if len(valid_cards_to_play) == 1 and isinstance(valid_cards_to_play[0], DrawCard):
            valid_cards_to_play = []
        features = {
            'num_playable_cards': len(valid_cards_to_play),
            'num_red': card_counts["Red"],
            'num_green': card_counts["Green"],
            'num_blue': card_counts["Blue"],
            'num_yellow': card_counts["Yellow"],
            'num_stop': card_counts["Stop"],
            'num_plus2': card_counts["+2"],
            'num_plus4': card_counts["+4"],
            'num_all_color': card_counts["Colors"], 
            'top_card': str(game.get_card_on_top()),
            'num_cards_left_in_deck': game.get_num_cards_left_in_deck(),
            'round': game.get_round(),
            'num_enemy_cards': game.get_next_player().get_num_of_cards_in_hand(),
            'direction': game.get_direction(),
            'num_colors_in_hand': sum(
                1 for count in [card_counts["Red"], card_counts["Green"], card_counts["Blue"], card_counts["Yellow"]] if
                count > 0),
            'num_cards_in_hand': len(self.hand),
            'is_game_over': game.get_game_over(),
            'player_instance': type(self).__name__
        }

        self.features = features
        return self.features

    def __str__(self) -> str:
        return f"{self.name}"

    def get_config(self):
        return {
            "type": "Player",
            "name": self.name,
            "class": self.__class__.__name__
        }

    def count_colors_in_hand(self):
        return {color: sum(1 for card in self.hand if card.color == color) for color in self.possible_colors}

    def valid_cards(self, card_taken=None) -> list:
        """Creates a list of cards that can be played. If there isn't any, bot takes a card"""
        valid_cards = []
        if card_taken is not None:
            if isinstance(card_taken, ColorCard):
                for color in self.possible_colors:
                    valid_cards.append(self.create_card_instance(card_taken.value, color))
                return valid_cards
            return [card_taken]

        if self.turns_to_stop != 0:
            valid_cards = self.collect_valid_cards_of_given_instance(StopCard)
            valid_cards.append(StopCard("Stop", "Stop"))
            return valid_cards if len(valid_cards) > 0 else [StopCard("Stop", "Stop")]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus4Card):
            valid_cards = self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        if self.cards_to_take != 0 and isinstance(self.card_on_top, Plus2Card):
            valid_cards = self.collect_valid_cards_of_given_instance(
                Plus2Card) + self.collect_valid_cards_of_given_instance(Plus4Card)
            return valid_cards if len(valid_cards) > 0 else [DrawCard()]

        valid_cards = self.collect_valid_cards_of_given_instance(Card)

        return valid_cards if len(valid_cards) > 0 else [DrawCard()]

    def collect_valid_cards_of_given_instance(self, instance):
        '''returns cards of given instance that can be played'''
        valid_cards_to_put = []

        for card in self.hand:
            if card.match(self.card_on_top) and isinstance(card, instance):
                if isinstance(card, ColorCard) and not isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        special_card = ColorCard()
                        special_card.change_color(color)
                        valid_cards_to_put.append(special_card)
                elif isinstance(card, Plus4Card):
                    for color in self.possible_colors:
                        special_card = Plus4Card()
                        special_card.change_color(color)
                        valid_cards_to_put.append(special_card)
                else:
                    valid_cards_to_put.append(card)
        return valid_cards_to_put
        
    def create_card_instance(self, card_value: str, card_color: str = None):
        if card_value == "+4":
            card = Plus4Card(card_value, card_color)
            if card_color == "Colors" or card_color == "Color":
                card.change_color(self.choose_color())
            else:
                card.change_color(card_color)

        elif card_value == "All":
            card = ColorCard(card_value, card_color)
            if card_color == "Colors" or card_color == "Color":
                card.change_color(self.choose_color())
            else:
                card.change_color(card_color)
        elif card_value == "Stop" and card_color is None:
            card = StopCard(card_value, card_value)
        elif card_value == "Stop" and card_color is not None:
            card = StopCard(card_value, card_color)
        elif card_value == "+2":
            card = Plus2Card(card_value, card_color)
        elif card_value == "Reverse":
            card = ReverseCard(card_value, card_color)
        elif card_value == "Draw":
            card = DrawCard()
        else:
            card = Card(card_value, card_color)
        return card

    def rich_str(self):
        return f":man:[bold purple]{self.name}[/]"

    def get_num_of_cards_in_hand(self):
        return len(self.hand)

    def hand_to_string(self):
        # Prints cards player has on hand
        str = f"Your hand: {len(self.hand)} cards\n|"
        for card in self.hand:
            str += f" { card.rich_str()} |"
        return str

    def move(self, card_taken = None, game=None):
        card_to_play = input().split(" ")

        if card_to_play[0] == "Surrender":  # Surrenders
            return SurrenderCard()
        elif card_to_play[0] == "Draw":  # Draws a card
            return DrawCard()
        elif card_to_play[0] == "Stop" and len(card_to_play) == 1:  # Players decides to be stopped
            return StopCard("Stop", "Stop")
        elif len(card_to_play) != 2:  # Checking if there are 2 components to a card
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move()
        elif card_to_play[1] not in ["Red", "Green", "Blue", "Yellow"]:
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move()
        elif card_taken is not None and card_to_play[0] != card_taken.value and (card_to_play[1] != card_taken.color or card_taken.color == "Colors"):
            print("You have to pick card you drawed!!")
            return self.move()
        elif card_to_play[0] == "+4":  # Looks for +4 cards in hand
            find_card = self.find_in_hand(value="+4")
            if find_card is False:
                self.console.print("It seems that you have given wrong values. Let's try again")
                return self.move()
            else:
                change_successful = find_card.change_color(card_to_play[1])
                if change_successful:
                    return find_card
                else:
                    self.console.print("It seems that you have given wrong values. Let's try again")
                    return self.move()
        elif card_to_play[0] == "All":
            find_card = self.find_in_hand(value="All")
            if find_card is False:
                self.console.print("It seems that you have given wrong values. Let's try again")
                return self.move()
            else:
                change_successful = find_card.change_color(card_to_play[1])
                if change_successful:
                    return find_card
                else:
                    self.console.print("It seems that you have given wrong values. Let's try again")
                    return self.move()
        else:
            find_card = Card(card_to_play[0], card_to_play[1])
            if find_card in self.hand:
                card = self.hand[self.hand.index(find_card)]
                return card
            else:
                self.console.print("You don't have this card on hand. Pick something else.")
                return self.move()


    def find_in_hand(self, color=None, value=None):
        if color is not None and value is not None:
            for card in self.hand:
                if card.color == color and card.value == value:
                    return card
        elif color is not None:
            for card in self.hand:
                if card.color == color:
                    return card
        else:
            for card in self.hand:
                if card.value == value:
                    return card
        return False

    def stop_player(self, turns_to_stop):
        self.stopped = True
        self.stop_status = turns_to_stop

    def update_stop_status(self):
        self.stop_status -= 1
        if self.stop_status == 0:
            self.stopped = False

    def has_won(self):
        return False if len(self.hand) != 0 else True

    def play_card(self, card):
        if isinstance(card, ColorCard):
            self.hand.remove(self.find_in_hand(value=card.value))
        elif isinstance(card, (DrawCard, SurrenderCard)):
            return
        elif isinstance(card, StopCard) and card.color == "Stop":
            return
        else:
            self.hand.remove(card)

