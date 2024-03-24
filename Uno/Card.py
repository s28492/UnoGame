class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0

    def __str__(self):
        return self.name

    def show_hand(self):
        cards = f"{self.name} hand:\n| "
        for card in self.hand:
            cards += f"{card} | "
        return cards

    def manage_stop(self):
        if self.stop_status > 1:
            self.stop_status -= 1
        else:
            self.stop_status -= 1
            self.stopped = False

    def wanna_stop(self):
        print(f"Stop turns: {self.stop_status}")
        have_stop = False
        for card in self.hand:
            if card.value == "Stop":
                have_stop = True
                break
        if have_stop:
            print("Wanna stop? [Yes], [No]")
            do_stop = input()
            while do_stop not in ["Yes", "No"]:
                print("Wrong anwser. Try again")
                do_stop = input()
            if do_stop == "Yes":
                return True
            elif do_stop == "No":
                return False
        return True

    def show_possible_cards(self, value=None, color=None):
        cards_to_play = ""
        if value is not None:
            for card in self.hand:
                cards_to_play += card if card.value == value else ""
        else:
            for card in self.hand:
                cards_to_play += card if card.color == value else ""
        return str

    def play_stop_card(self):
        print("Cards you can play: ")
        print(self.show_possible_cards(value="Stop"))

    def player_status(self):
        able_to_play = True
        if self.stop_status > 0 and self.stopped is False:
            self.stopped = self.wanna_stop()
            able_to_play = not self.stopped
        return able_to_play

    def play_move(self, top_card_on_pile):
        print(f"Card on the top of the pile: {top_card_on_pile}")
        print(self.show_hand())
        print("Write what you wanna play: [Value Color], [Draw], [Surrender]")

        value = input()
        if value == "Draw":
            value = "-1 Draw"
        elif value == "Surrender":
            value = "-1 Surrender"
        card = value.split(" ")
        try:
            card = Card(card[0], card[1])
        except:
            print("You gave me wrong values you sneaky bastard!")
            return self.play_move(top_card_on_pile)
        if card.color == "Draw" or card.color == "Surrender":
            return card
        elif card in self.hand:
            card = self.hand.pop(self.hand.index(card))
            return card
        else:
            print("It seems that you don't have this card on hand. Let's try again:")
            return self.play_move(top_card_on_pile)
    # return self.hand.pop()


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        return f"{self.value} {self.color}"

    def __eq__(self, other):
        if (self.value == other.value) and (self.color == other.color):
            return True
        else:
            return False

    def play(self, game, player: Player):
        return self

    def match(self, other):
        if self.value == other.value or self.color == other.color or other.color == "Colors":
            print("Primary match true")
            return True
        else:
            print("primary match false")
            return False


'''elif type(other) != type(self):
            print("Here")
            return other.match(self)'''


class ReverseCard(Card):
    # Specjalne zachowanie dla karty Reverse
    def __init__(self, value, color):
        super().__init__(value, color)

    def play(self, game, player):
        game.direction *= -1
        return self


'''    def match(self, other):
        if self.color == other.color or other.color == "Colors":
            return True
            
        else:
            return False'''


class StopCard(Card):
    def __init__(self, value, color):
        super().__init__(value, color)

    def play(self, game, player):
        game.players[(game.player_index + 1) % len(game.players)].stop_status = player.stop_status + 1
        player.stop_status = 0
        return self


class Plus2Card(Card):
    def __init__(self, value, color):
        super().__init__(value, color)


class Plus4Card(Card):
    def __init__(self, value, color):
        super().__init__(value, color)


class ColorCard(Card):
    def __init__(self, color, value):
        super().__init__(color, value)

    def match(self, other):
        if other.color in ["Red", "Green", "Blue", "Yellow"]:
            print("All Collors true")
            return True

    def play(self, game, player):
        print("Alrigth, what color you command?")
        self.color = input()
        while self.color not in game.colors:
            print("Wrong color, try again:")
            self.color = input()
        return self
