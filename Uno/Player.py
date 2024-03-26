from Card import Card, SurrenderCard, DrawCard
class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stop_status = 0
        self.stopped = False
        self.takes_status = 0

    def __str__(self):
        return f"{self.name}"

    def show_hand(self):
        str = "Your hand:\n| "
        for card in self.hand:
            str += f"{card} |"
        print(str)

    @staticmethod
    def player_decision():
        decision = input()
        while decision not in ["Yes", "No"]:
            decision = input("Sorry wrong input. Try again")
        return decision

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
