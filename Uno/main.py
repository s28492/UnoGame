'''
@author Cyprian Szewczak s28492
Documentation:

create_game_with_players(*players) -> Game
This function creates game with initialized starting state of a game

def main() -> None
This function creates lobby that allows player to set players and bots and starts the game

def start_bot_thread(bot: Bot, game: Game) -> None:
This function starts bot thread

Total lanes of code: 706
'''

from Player import Player
from Bot import Bot
from Game import Game
from rich.console import Console

console = Console()


def create_game_with_players(*players) -> Game:
    """returns game with initialized starting state"""
    return Game(*players)


def main() -> None:
    """Starts the game"""
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    bots = []
    game = None

    console.print("[bold magenta]Welcome to UNO game![/bold magenta]")
    console.print("1. Play with other humans.")
    console.print("2. Watch bots playing with each other.")
    console.print("3. Play with humans and bots.")

    choice = console.input("[bold green]Pick an option (1-3): [/bold green]")

    if choice == "1":
        player_names = console.input("Input players names separated by coma: ").split(',')
        players = [Player(name.strip()) for name in player_names]
        game = create_game_with_players(*players)
    elif choice == "2":
        num_bots = int(console.input("How many bots should play? "))
        bots = [Bot(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
        game = create_game_with_players(*bots)
    elif choice == "3":
        player_names = console.input("Input players names separated by coma: ").split(',')
        num_bots = int(console.input("How many bots should play? "))
        players = [Player(name.strip()) for name in player_names]
        bots = [Bot(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
        game = create_game_with_players(*players, *bots)
    else:
        console.print("[bold red]Wrong choice![/bold red]\nLet's try again...\n")
        main()

    game.play()



if __name__ == "__main__":
    main()
