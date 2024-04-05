import time

from UnoGame.Uno.Player import Player
from UnoGame.Uno.Bot import Bot
from UnoGame.Uno.Game import Game
from rich import print
import threading
from rich.console import Console


def main():
    bot1 = Bot("Beta")
    bot2 = Bot("Omega")
    bot3 = Bot("Andromeda")
    bot4 = Bot("Mars")
    bot5 = Bot("Polak")
    bot6 = Bot("Ziemniak")
    player2 = Player("Margarett Tatcher")
    player3 = Player("Trzeci")
    game = Game(bot1, bot2, bot3, bot4, bot5, bot6)
    thread1 = threading.Thread(target=bot1.update_data, daemon=True, args=[game])
    thread2 = threading.Thread(target=bot2.update_data, daemon=True, args=[game])
    thread3 = threading.Thread(target=bot3.update_data, daemon=True, args=[game])
    thread4 = threading.Thread(target=bot4.update_data, daemon=True, args=[game])
    thread5 = threading.Thread(target=bot5.update_data, daemon=True, args=[game])
    thread6 = threading.Thread(target=bot6.update_data, daemon=True, args=[game])
    thread7 = threading.Thread(target=game.play, daemon=False)

    thread1.start()
    thread2.start()


    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()

    thread7.start()


if __name__ == "__main__":
    main()
