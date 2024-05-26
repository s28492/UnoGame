from Card import Card, SurrenderCard, DrawCard, StopCard, Plus4Card, ColorCard
from rich.console import Console


class Player:
    def __init__(self, name):
        # Initialize player
        self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0
        self.first_taken = False
        self.console = Console()
        self.features = {}

    def get_features(self):
        return self.features

    def count_cards(self):
        card_dict = {
            "Red": 0,
            "Green": 0,
            "Blue": 0,
            "Yellow": 0,
            "Stop": 0,
            "+2": 0,
            "+4": 0,

        }
        for card in self.hand:
            if card.color in card_dict:
                card_dict[card.color] += 1
            if card.value in card_dict:
                card_dict[card.value] += 1
        return card_dict

    def extract_features(self, game):
        card_counts = self.count_cards()

        features = {
            'num_red': card_counts["Red"],
            'num_green': card_counts["Green"],
            'num_blue': card_counts["Blue"],
            'num_yellow': card_counts["Yellow"],
            'num_stop': card_counts["Stop"],
            'num_plus2': card_counts["+2"],
            'num_plus4': card_counts["+4"],
            'top_card': str(game.get_card_on_top()),
            'num_cards_left_in_deck': game.get_num_cards_left_in_deck(),
            'round': game.get_round(),
            'num_enemy_cards': game.get_next_player().get_count_cards_in_hand(),
            'direction': game.get_direction(),
            'num_colors_in_hand': sum(
                1 for count in [card_counts["Red"], card_counts["Green"], card_counts["Blue"], card_counts["Yellow"]] if
                count > 0),
            'num_cards_in_hand': len(self.hand)
        }

        self.features = features

    def __str__(self) -> str:
        return f":smile:[magenta]{self.name}[/]"

    def get_count_cards_in_hand(self):
        return len(self.hand)

    def show_hand(self):
        # Prints cards player has on hand
        str = f"Your hand: [cyan]{len(self.hand)} cards[/]\n| "
        for card in self.hand:
            str += f"[bold {card.color.lower()}]{card}[/] |"

        self.console.print(str, style="bold")

    def get_game_state(self, game):
        self.players, self.pile, self.card_on_top, self.direction \
            , self.turns_to_stop, self.cards_to_take, self.first_taken = game.get_state()


    def move(self):
        # Takes
        self.show_hand()
        card_to_play = input()
        card_to_play = card_to_play.split(" ")
        if card_to_play[0] == "Surrender":  #Surrenders
            return SurrenderCard()
        elif card_to_play[0] == "Draw": #Draws a card
            return DrawCard()
        elif card_to_play[0] == "Stop" and len(card_to_play) == 1:  #Players decides to be stopped
            return StopCard("Stop", "Stop")
        elif len(card_to_play) != 2:    #Checking if there are 2 components to a card
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move()
        elif card_to_play[1] not in ["Red", "Green", "Blue", "Yellow"]:
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move()
        elif card_to_play[0] == "+4":   #Looks for +4 cards in hand
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
