from Card import Card, SurrenderCard, DrawCard
from rich.console import Console


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0
        self.console = Console()
    def __str__(self):
        return f":smile:[magenta]{self.name}[/]"

    def show_hand(self):
        str = f"Your hand: {len(self.hand)}\n| "
        for card in self.hand:
            str += f"[bold {card.color.lower()}]{card}[/] |"

        self.console.print(str, style="bold")

    def player_decision(self) -> str:
        decision = input()
        while decision not in ["Yes", "No"]:
            decision = input("Sorry wrong input. Try again")
        return decision

    def choose_color(self):
        new_color = input("What color you want?")
        while new_color not in ["Red", "Green", "Blue", "Yellow"]:
            new_color = input("Wrong color. Let's try again")
        return new_color

    def move(self):
        card_to_play = input()
        card_to_play = card_to_play.split(" ")
        if card_to_play[0] == "Surrender":
            return SurrenderCard()
        elif card_to_play[0] == "Draw":
            return DrawCard()
        elif len(card_to_play) != 2:
            print("It seems that you have given wrong values. Let's try again")
            return self.move()
        else:
            find_card = Card(card_to_play[0], card_to_play[1])
            if find_card in self.hand:
                card = self.hand[self.hand.index(find_card)]
                return card
            else:
                print("You don't have this card on hand. Pick something else.")
                return self.move()
