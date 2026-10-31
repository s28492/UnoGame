from Uno.game.Card import Card, SurrenderCard, DrawCard, StopCard, ColorCard
from rich.console import Console
from Uno.players.Player import Player

console = Console()


class HumanPlayer(Player):
    def __init__(self, name: str = ""):
        super().__init__(name)
        self.console = console

    def rich_str(self):
        return f":man:[bold purple]{self.name}[/]"

    def get_config(self):
        return {
            "type": "Human",
            "name": self.name,
            "class": self.__class__.__name__
        }
    
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

    def hand_to_string(self):
        # Prints cards player has on hand
        str = f"Your hand: {len(self.hand)} cards\n|"
        for card in self.hand:
            str += f" { card.rich_str()} |"
        return str

    def move(self, first_card_taken=None, game=None, card_taken=None):
        if first_card_taken is None and card_taken is not None:
            first_card_taken = card_taken
        card_to_play = input().split(" ")

        if card_to_play[0] == "Surrender":
            return SurrenderCard()
        elif card_to_play[0] == "Draw":
            return DrawCard()
        elif card_to_play[0] == "Stop" and len(card_to_play) == 1:
            return StopCard("Stop", "Stop")
        elif len(card_to_play) != 2:
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
        elif card_to_play[1] not in ["Red", "Green", "Blue", "Yellow"]:
            self.console.print("It seems that you have given wrong values. Let's try again")
            return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
        elif first_card_taken is not None and card_to_play[0] != first_card_taken.value and (card_to_play[1] != first_card_taken.color or first_card_taken.color == "Colors"):
            print("You have to pick card you drawed!!")
            return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
        elif card_to_play[0] == "+4":
            find_card = self.find_in_hand(value="+4")
            if find_card is False:
                self.console.print("It seems that you have given wrong values. Let's try again")
                return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
            else:
                change_successful = find_card.change_color(card_to_play[1])
                if change_successful:
                    return find_card
                else:
                    self.console.print("It seems that you have given wrong values. Let's try again")
                    return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
        elif card_to_play[0] == "All":
            find_card = self.find_in_hand(value="All")
            if find_card is False:
                self.console.print("It seems that you have given wrong values. Let's try again")
                return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
            else:
                change_successful = find_card.change_color(card_to_play[1])
                if change_successful:
                    return find_card
                else:
                    self.console.print("It seems that you have given wrong values. Let's try again")
                    return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
        else:
            find_card = Card(card_to_play[0], card_to_play[1])
            if find_card in self.hand:
                card = self.hand[self.hand.index(find_card)]
                return card
            else:
                self.console.print("You don't have this card on hand. Pick something else.")
                return self.move(first_card_taken=first_card_taken, game=game, card_taken=card_taken)
