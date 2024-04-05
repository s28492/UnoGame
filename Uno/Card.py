class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def play(self, game):
        game.players[game.index_of_a_player].hand.remove(self)
        return self

    def match(self, other):
        if self.value == other.value or self.color == other.color or other.color == "Colors":
            return True
        else:
            return False

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
    def match(other: Card) -> bool:
        return True

    @staticmethod
    def play(game) -> Card:
        player = game.get_player()
        print(f"Player: {player} has surrendered")

        game.drop_player(player, did_not_surrender=False)
        return game.card_on_top


class DrawCard:
    def __init__(self):
        self.value = "Draw"
        self.color = "Draw"

    def __eq__(self, other):
        return True

    def __str__(self):
        return f"{self.value}"

    @staticmethod
    def match(other: Card) -> bool:
        return True

    @staticmethod
    def play(game) -> Card:
        game.take_first_card(game.players[game.index_of_a_player])
        return game.card_on_top


class ReverseCard(Card):
    def __init__(self, value, color):
        super().__init__(value, color)

    def play(self, game):
        game.direction *= -1
        game.players[game.index_of_a_player].hand.remove(self)
        return self


class StopCard(Card):
    def __init__(self, value, color):
        super().__init__(value, color)

    def play(self, game):
        game.turns_to_stop += 1
        game.get_player().hand.remove(self)
        return self


class Plus2Card(Card):
    def __init__(self, value, color):
        super().__init__(value, color)
        self.value = "+2"

    def play(self, game):
        game.cards_to_take += 2
        game.players[game.index_of_a_player].hand.remove(self)
        return self


class ColorCard(Card):
    def __init__(self, value, color):
        super().__init__(color, value)
        self.value = "All"
        self.color = "Colors"

    def __str__(self):
        if self.color == "Colors":
            return "[red]A[/][rgb(255,165,0)]l[/][yellow]l[/] [rgb(0,255,0)]C[/][green]o[/][cyan]l[/][blue]o[/][rgb(255,0,255)]r[/][magenta]s[/]"
        return f"{self.value} {self.color}"


    def play(self, game):
        self.change_color(game.players[game.index_of_a_player])
        game.players[game.index_of_a_player].hand.remove(self)
        return self

    def match(self, other):
        return True

    def change_color(self, player):
        self.color = player.choose_color()


class Plus4Card(ColorCard):
    def __init__(self, value, color):
        super().__init__(value, color)
        self.value = "+4"
        self.color = "Colors"

    def __str__(self):
        if self.color == "Colors":
            return "[red]+[/][rgb(255,165,0)]4[/] [rgb(0,255,0)]C[/][green]o[/][cyan]l[/][blue]o[/][rgb(255,0,255)]r[/][magenta]s[/]"
        return f"{self.value} {self.color}"

    def play(self, game):
        game.cards_to_take += 4
        self.change_color(game.players[game.index_of_a_player])
        game.players[game.index_of_a_player].hand.remove(self)
        return self
