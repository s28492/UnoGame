'''
@author Cyprian Szewczak s28492

'''
import time

from Uno.players.Player import Player
from Uno.players.Bot import Bot
from Uno.players.RandomBot import BotRandom
from Uno.AIPlayers.ID3Bot import ID3Bot
from Uno.AIPlayers.MonteCarloTreeSearch.MCTSBot import MCTSBot

from Uno.game.Game import Game
from rich.console import Console
import random

console = Console()


def create_game_with_players(players, has_human_player:bool = False) -> Game:
    """returns game with initialized starting state"""
    return Game(players, has_human_player)


def main() -> None:
    """Starts the game"""
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
    bots = []
    game = None
    console.print("\n[bold magenta]Welcome to UNO game![/bold magenta]",justify="center", end="\n\n")
    console.print("1. Play with other humans.", justify="center")
    console.print("2. Watch bots playing with each other.", justify="center")
    console.print("3. Play with humans and bots.", justify="center")
    console.print(
        "4. Play with bots and Dima (AI).", justify="center"
    )
    console.print("[bold gold]4. Dawaj to Dima!!![/]", justify="center", end="\n\n")


    choice = console.input("[bold green]Pick an option (1-4): [/bold green]")

    if choice == "1":
        player_names = console.input("Input players names separated by coma: ").split(',')
        players = [Player(name.strip()) for name in player_names]
        game = create_game_with_players(players, True)
    elif choice == "2":
        num_bots = int(console.input("How many bots should play? "))
        bots = [Bot(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
        game = create_game_with_players(bots)
    elif choice == "3":
        player_names = console.input("Input players names separated by coma: ").split(',')
        num_bots = int(console.input("How many bots should play? "))
        players = [Player(name.strip()) for name in player_names]
        bots = [Bot(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
        game = create_game_with_players(players+bots, True)
    elif choice == "4":
        bots = [ Player("Dima"), MCTSBot(bot_names.pop(), 50_000, 1.9)]
        random.shuffle(bots)
        game = create_game_with_players(bots)
        game.play()
    else:
        console.print("[bold red]Wrong choice![/bold red]\nLet's try again...\n")
        main()
    _, winner = game.play()
    console.print(f"[bold]And the winner is [yellow] {winner}[/yellow][/bold]")



def start_2_bot_games():
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
    bots = []
    game = None

    num_bots = 2
    bots = [BotRandom(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
    game = create_game_with_players(bots)
    game.play()

def start_many_games():
    number_of_games = 10
    start_time = time.time()
    for i in range(number_of_games):
        start_2_bot_games()
    end_time = time.time()
    print(f"{number_of_games} games played in: {end_time-start_time}")

if __name__ == "__main__":
    main()