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
import os
import time
from datetime import datetime

from Player import Player
from Bot import Bot
from Bot_Random import BotRandom
from Game import Game
from rich.console import Console
import random
import pandas as pd
from collections import Counter

console = Console()

def create_game_with_players(players) -> Game:
    """returns game with initialized starting state"""
    return Game(players)


def main() -> None:
    """Starts the game"""
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
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
        game = create_game_with_players(bots)
    elif choice == "3":
        player_names = console.input("Input players names separated by coma: ").split(',')
        num_bots = int(console.input("How many bots should play? "))
        players = [Player(name.strip()) for name in player_names]
        bots = [Bot(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
        game = create_game_with_players(*players, *bots)
    else:
        console.print("[bold red]Wrong choice![/bold red]\nLet's try again...\n")
        main()

who_won = []
def start_2_bot_games():
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
    bots = []
    game = None

    num_bots = 2
    bots = [BotRandom(bot_names.pop()), Bot(bot_names.pop())]
    random.shuffle(bots)
    game = create_game_with_players(bots)
    return game.play()

def start_many_games():
    number_of_games = 10_000
    games_data = pd.DataFrame()
    start_time = time.time()
    who_won = []
    for i in range(number_of_games):
        game = start_2_bot_games()
        pd.concat([games_data, pd.DataFrame(game[0])])
        who_won.append(game[1])
    end_time = time.time()
    save_to_csv(games_data, 'uno_game.csv')
    print(f"Score: {Counter(who_won)}")
    print(f"{number_of_games} games played in: {end_time-start_time}")


def save_to_csv(data, filename='uno_game.csv', folder='games_data'):
    # If the default filename is used, append a timestamp
    if filename == 'uno_game.csv':
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{filename}"

    # Create the full filepath
    filepath = os.path.join(folder, filename)

    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create a DataFrame from the new data
    new_df = pd.DataFrame(data)

    if os.path.exists(filepath):
        # If the file exists, read the existing data
        existing_df = pd.read_csv(filepath)
        # Concatenate the existing data with the new data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Save the combined data back to the file
        combined_df.to_csv(filepath, index=False)
    else:
        # If the file does not exist, create a new file with the new data
        new_df.to_csv(filepath, index=False)

if __name__ == "__main__":
    start_many_games()
