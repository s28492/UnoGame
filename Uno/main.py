import os
import time
from datetime import datetime
from Player import Player
from Bot import Bot
from Bot_Random import BotRandom
from BasicLogicBot import BasicLogicBot
from AgressiveBot import AgressiveBot
from Game import Game
from rich.console import Console
import random
import pandas as pd
from collections import Counter
from rich.progress import track
from rich.progress import Progress
from multiprocessing import Pool

console = Console()

def create_game_with_players(*players) -> Game:
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

def start_2_bot_games():
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
    bots = []
    game = None

    num_bots = 2
    bots = [BasicLogicBot(bot_names.pop()), AgressiveBot(bot_names.pop())]
    random.shuffle(bots)
    game = create_game_with_players(*bots)
    return game.play()

def start_many_games():
    number_of_games = 10_000
    games_data = pd.DataFrame()
    start_time = time.time()
    who_won = []
    iterator = 0
    with Progress() as progress:
        task = progress.add_task("Playing games...", total=number_of_games)

        while not progress.finished:
            iterator += 1
            progress.update(task, advance=1)
            game = start_2_bot_games()
            game_df = pd.DataFrame(game[0])
            games_data = pd.concat([games_data, game_df], ignore_index=True)
            who_won.append(game[1])
            if iterator % 10_000:
                save_to_csv(games_data, 'uno_game.csv')
                games_data.drop(games_data.index, inplace=True)

    end_time = time.time()
    save_to_csv(games_data, 'uno_game.csv')
    win_count = Counter(who_won)
    print(f"Score: {win_count}")
    print(f"Proportion: {round(list(win_count.values())[0]/(list(win_count.values())[0]+list(win_count.values())[1]), 2)}%")
    print(f"{number_of_games} games played in: {round(end_time - start_time)} seconds")

def save_to_csv(data, filename='uno_game.csv', folder='games_data'):
    # If the default filename is used, append a timestamp
    if filename == 'uno_game.csv':
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{filename}"

    # Create the full filepath
    filepath = os.path.join(folder, filename)
    #print(f"Saving data to: {filepath}")

    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create a DataFrame from the new data
    new_df = pd.DataFrame(data)

    if os.path.exists(filepath):
        #print("File exists. Appending data.")
        # If the file exists, read the existing data
        existing_df = pd.read_csv(filepath)
        # Concatenate the existing data with the new data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Save the combined data back to the file
        combined_df.to_csv(filepath, index=False)
    else:
        #print("File does not exist. Creating new file.")
        # If the file does not exist, create a new file with the new data
        new_df.to_csv(filepath, index=False)

if __name__ == "__main__":
    start_many_games()
