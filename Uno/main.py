import os
import time
from datetime import datetime
from Uno.players.Player import Player
from Uno.players.Bot import Bot
from Uno.players.Bot_Random import BotRandom
from Uno.players.BasicLogicBot import BasicLogicBot
from Uno.players.AgressiveBot import AgressiveBot
from Uno.players.BLBUpgradedColorChoosing import BLBUpgradedColorChoosing
from Uno.DecisionTrees.ID3Bot import ID3Bot
from Uno.DecisionTrees.ID3Tree import ID3Tree
from Uno.game.Game import Game
from rich.console import Console
import random
import pandas as pd
from collections import Counter
from rich.progress import Progress

console = Console()
bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]


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


def start_2_bot_games(matchup):
    random.shuffle(bot_names)
    game = create_game_with_players(*matchup)
    return game.play()

def create_instances(bots):
    names = bot_names.copy()
    random.shuffle(names)
    instances_to_return = []
    for bot in bots:
        if bot == "BasicLogicBot":
            instances_to_return.append(BasicLogicBot(names.pop()))
        elif bot == "AgressiveBot":
            instances_to_return.append(AgressiveBot(names.pop()))
        elif bot == "ID3Bot":
            name = names.pop()
            instances_to_return.append(ID3Bot(name))
        else:
            instances_to_return.append(BLBUpgradedColorChoosing(names.pop()))
    return instances_to_return

def start_many_games(matchups, number_of_games = 1_000):
    games_data = pd.DataFrame()
    who_won_tables = []
    for _ in range(len(matchups)):
        who_won_tables.append([])

    start_time = time.time()
    for i in range(number_of_games):
        for j, matchup in enumerate(matchups):
            bots = create_instances(matchup)
            #print("Starting games...")
            game = start_2_bot_games(bots)
            current_game_data = assign_did_win(pd.DataFrame(game[0]))
            games_data = pd.concat([games_data, current_game_data], ignore_index=True)
            who_won_tables[j].append(game[1])
        if (i % 2_000 == 0 and i != 0) or i == number_of_games -1:
            file_name = save_to_csv(games_data, 'uno_game.csv')
            games_data.drop(games_data.index, inplace=True)
            print(f"{i} Saved to file '{file_name}'...")

    end_time = time.time()
    for i in range(len(who_won_tables)):
        win_count = Counter(who_won_tables[i])
        print(f"\nScore: {win_count}")
        print(f"Proportion: {round(list(win_count.values())[0] / (list(win_count.values())[0] + list(win_count.values())[1]), 2)}%")
    print("Time taken to play:", round((end_time - start_time) / 60, 2), "min")


def assign_did_win(df):
    df['did_win'] = False  # Najpierw ustaw wszystkie wartości na False
    games = df['game_id'].unique()
    for game in games:
        game_df = df[df['game_id'] == game]
        winning_indices = game_df[game_df['is_game_over']].index
        for idx in winning_indices:
            player_index = game_df.loc[idx, 'index_of_a_player']
            df.loc[(df['game_id'] == game) & (df['index_of_a_player'] == player_index), 'did_win'] = True
    return df

def save_to_csv(data, filename='uno_game.csv', folder='games_data'):
    # If the default filename is used, append a timestamp
    if filename == 'uno_game.csv':
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{filename}"


    # Create the full filepath
    filepath = os.path.join(folder, filename)
    # print(f"Saving data to: {filepath}")

    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create a DataFrame from the new data
    new_df = pd.DataFrame(data)

    if os.path.exists(filepath):
        # print("File exists. Appending data.")
        # If the file exists, read the existing data
        existing_df = pd.read_csv(filepath)
        # Concatenate the existing data with the new data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Save the combined data back to the file
        combined_df.to_csv(filepath, index=False)
    else:
        # print("File does not exist. Creating new file.")
        # If the file does not exist, create a new file with the new data
        new_df.to_csv(filepath, index=False)
    return filename


if __name__ == "__main__":
    start_many_games([["ID3Bot", "BasicLogicBot"],
                      ["AgressiveBot", "ID3Bot"],
                      ["ID3Bot", "BLBUpgradedColorChoosing"]]
                     , 10_000)
