from Card import Game, Player


def main():
    player1 = Player("Krzysztof")
    player2 = Player("Margarett Tatcher")
    game = Game(player1, player2)
    game.play()



if __name__ == "__main__":
    main()