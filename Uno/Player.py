"""
@author Cyprian Szewczak s2849
"""

from Card import Card, SurrenderCard, DrawCard
from rich.console import Console
import re


class Player:
    def __init__(self, name):
        """Initialize player"""
        self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0
        self.console = Console()

    def __str__(self) -> str:
        return f":smile:[magenta]{self.name}[/]"

    def show_hand(self):
        """Prints cards player has on hand"""
        str = f"Your hand: [cyan]{len(self.hand)} cards[/]\n| "
        for card in self.hand:
            str += f"[bold {card.color.lower()}]{card}[/] |"

        self.console.print(str, style="bold")

    def player_decision(self) -> str:
        """Takes player input "Yes" or "No" and returns it to the game"""
        decision = input()
        while decision not in ["Yes", "No"]:
            decision = input("Sorry wrong input. Try again")
        return decision

    def choose_color(self):
        """Takes player input on color of his Color card and returns it"""
        new_color = input("What color you want?")
        possible_colors = "Red Green Blue Yellow"
        # Looks if color in possible colors. If not then tries again
        while re.search(new_color, possible_colors, flags=0) is None:
            new_color = input("Wrong color. Let's try again")
        return new_color

    def move(self):
        """Takes a move of a player and returns it if valid"""
        card_to_play = input()
        card_to_play = card_to_play.split(" ")
        # Checks if card is SurrenderCard and returns it if yes
        if card_to_play[0] == "Surrender":
            return SurrenderCard()
        # Checks if card is DrawCard and returns it if yes
        elif card_to_play[0] == "Draw":
            return DrawCard()
        # Checks if card has 2 attributes and runs again method if yes
        elif len(card_to_play) != 2:
            print("It seems that you have given wrong values. Let's try again")
            return self.move()
        else:
            # Creates a card from player input and checks if on hand
            find_card = Card(card_to_play[0], card_to_play[1])
            if find_card in self.hand:
                card = self.hand[self.hand.index(find_card)]
                return card
            else:
                print("You don't have this card on hand. Pick something else.")
                return self.move()
