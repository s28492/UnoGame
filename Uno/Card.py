"""
@author Cyprian Szewczak s2849
"""
from rich.console import Console

console = Console()
class Card:

    def __init__(self, value: str, color: str):
        """Initializes a card"""
        self.value = value
        self.color = color

    def play(self, game):
        """Removes itself from player hand"""
        return self

    def match(self, other):
        """Checks if value or color match with the other"""
        if self.value == other.value or self.color == other.color or other.color == "Colors":
            return True
        else:
            return False

    def img_url(self):
        return f"uno_card-{self.color.lower()}{self.value.lower()}.png"

    def __str__(self):
        return f"{self.value} {self.color}"

    def __eq__(self, other):
        if (self.value == other.value) and (self.color == other.color):
            return True
        else:
            return False


class SurrenderCard:
    def __init__(self):
        self.value = "Surrender"
        self.color = "Surrender"

    def __eq__(self, other):
        return True

    def __str__(self):
        return f"{self.value}"

    @staticmethod
    def match(other) -> bool:
        """returns true"""
        return True

    @staticmethod
    def play(game) -> Card:
        """Drops player from game. Returs card on top of a pile"""
        player = game.get_player()
        console.print(f"Player: {player} has surrendered")

        game.drop_player(player, did_not_surrender=False)
        return game.card_on_top


class DrawCard:
    def __init__(self):
        self.value = "Draw"
        self.color = "Draw"

    def __eq__(self, other):
        return False

    def __str__(self):
        return f"{self.value}"

    @staticmethod
    def match(other: Card) -> bool:
        """:returns true"""
        return True

    @staticmethod
    def play(game) -> Card:
        """:returns card on top of the pile"""
        return game.card_on_top


class ReverseCard(Card):
    def __init__(self, value: str, color: str):
        super().__init__(value, color)


    def play(self, game):
        """Reverses the game direction, removes itself from player hand and returns itself"""
        game.change_game_direction()
        return self


class StopCard(Card):
    def __init__(self, value: str, color: str):
        super().__init__(value, color)

    def img_url(self):
        return f"uno_card-{self.color.lower()}skip.png"

    def play(self, game):
        """Adds 1 to game.turns_to_stop, removes itself from player hand and returns itself"""
        game.add_turns_to_stop()
        return self


class Plus2Card(Card):
    def __init__(self, value: str, color: str):
        super().__init__(value, color)
        self.value = "+2"

    def img_url(self):
        return f"uno_card-{self.color.lower()}draw2.png"

    def play(self, game):
        """Adds 2 to game.cards_to_take, removes itself from player hand and returns itself"""
        game.add_cards_to_take(2)
        return self


class ColorCard(Card):
    def __init__(self, value, color):
        super().__init__(color, value)
        self.value = "All"
        self.color = "Colors"

    def __str__(self):
        if self.color == "Colors":
            return "[red]A[/][rgb(255,165,0)]l[/][yellow]l[/] [rgb(0,255,0)]C[/][green]o[/][cyan]l[/][blue]o[/][rgb(" \
                   "255,0,255)]r[/][magenta]s[/] "
        return f"{self.value} {self.color}"

    def img_url(self):
        return f"uno_card-wildchange.png"

    def play(self, game):
        """Changes color of itself, removes itself from player hand and returns itself"""
        return self

    def match(self, other):
        """:returns True"""
        return True

    def change_color(self, color):
        """Changes color of itself"""
        if color in ["Red", "Green", "Blue", "Yellow"]:
            self.color = color
            return True
        else:
            return False


class Plus4Card(ColorCard):
    def __init__(self, value: str, color: str):
        super().__init__(value, color)
        self.value = "+4"
        self.color = "Colors"

    def __str__(self):
        if self.color == "Colors":
            return "[red]+[/][rgb(255,165,0)]4[/] [rgb(0,255,0)]C[/][green]o[/][cyan]l[/][blue]o[/][rgb(255,0," \
                   "255)]r[/][magenta]s[/] "
        return f"{self.value} {self.color}"

    def img_url(self):
        return f"uno_card-wilddraw4.png"

    def play(self, game):
        """Changes color of itself, adds +4 to cards_to_take, removes itself from player hand and returns itself"""
        game.add_cards_to_take(4)
        return self
