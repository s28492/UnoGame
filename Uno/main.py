from UnoGame.Uno.Player import Player
from UnoGame.Uno.Game import Game



def main():
    player1 = Player("Pierwszy")
    player2 = Player("Margarett Tatcher")
    player3 = Player("Trzeci")
    #player4 = Player("Czwarty")
    game = Game(player1, player2, player3)
    game.play()




if __name__ == "__main__":

    main()