import os
import time
import yaml
import random
import pandas as pd
from src.utils import open_config
from datetime import datetime
from Uno.players.RandomBot import BotRandom
from Uno.players.BasicLogicBot import BasicLogicBot
from Uno.players.AgressiveBot import AgressiveBot
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.DecisionTrees.C4_5Tree import C4_5Tree
from Uno.AIPlayers.NaiveBayesianBot import NaiveBayesianBot
from Uno.AIPlayers.MonteCarloTreeSearch.MCTSBot import MCTSBot
from Uno.AIPlayers.C4_5BaggingEnsemble import C4_5BaggingEnsebleBot

from Uno.game.Game import Game
from rich.console import Console
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter

console = Console()
bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]

pd.set_option('future.no_silent_downcasting', True)

def create_game_with_players(*players) -> Game:
    """returns game with initialized starting state"""
    return Game(players)

def create_instances(bots):
    names = bot_names.copy()
    random.shuffle(names)
    instances_to_return = []

    configs = open_config()

    for bot in bots:
        if bot == "BasicLogicBot":
            instances_to_return.append(BasicLogicBot("BasicLogicBot"))
        elif bot == "AgressiveBot":
            instances_to_return.append(AgressiveBot("AgressiveBot"))
        elif bot == "RandomBot":
            instances_to_return.append(BotRandom("BotRandom"))
        elif bot == "C4_5Bot":
            instances_to_return.append(C4_5Bot())
        elif bot == "NaiveBayesianBot1":
            name = "NaiveBayesianBot1"
            pass 
        elif bot == "C4_5BaggingBot":
            name = "C4_5BaggingBot"
            bot = C4_5BaggingEnsebleBot(name, "Uno/DecisionTrees/BaggingTrees/n10_d1_sp0.63_dseTrue") 
            instances_to_return.append(bot)
        elif bot == "MCTSBot":
            name = configs["mcts"]["name"]
            number_of_simulations = configs["mcts"]["number_of_games"]
            c_param = configs["mcts"]["c_parameter"]
            bot: MCTSBot = MCTSBot(name, num_of_simulations=number_of_simulations, c_param=c_param)
            instances_to_return.append(bot)
            
    return instances_to_return

import uuid
from Uno.ReportingUtils import ReportGenerator

def play_game(matchup):
    bots = create_instances(matchup)
    
    start_ts = time.time()
    game_result = start_2_bot_games(bots)
    end_ts = time.time()
    duration = (end_ts - start_ts) / 60    
    bots.clear()
    current_game_data = assign_did_win(pd.DataFrame(game_result[0]))
    winner = game_result[1].name
    return current_game_data, winner

def start_2_bot_games(matchup):
    game = create_game_with_players(*matchup)
    return game.play()


def start_many_games(matchup, number_of_games=1000, number_of_processes=5):
    manager = Manager()
    games_data = manager.list()
    who_won = manager.list()

    def collect_results(result):
        current_game_data, winner = result
        games_data.append(current_game_data)
        who_won.append(winner)

    start_time = time.time()
    num_of_processes = number_of_processes if number_of_processes <= cpu_count() else cpu_count()
    print("Games starting...")
    try:
        with Pool(processes=num_of_processes) as pool:
            results = [pool.apply_async(play_game, (matchup,), callback=collect_results) for _ in range(number_of_games)]
            pool.close()
            pool.join()
    except Exception as e:
        raise Exception(f"Error occurred while playing games: {e}")

    df = pd.concat(list(games_data))
    file_name = save_to_csv(df, 'uno_game.csv')
    print(f"Saved to file '{file_name}'...")

    win_count = Counter(who_won)
    win_rates = {}
    for bot_name, count in win_count.items():
        percentage = round((count / number_of_games) * 100, 2)
        print(f"{bot_name}: {count} wins, {percentage}%")
        win_rates[bot_name] = {
            "wins": count,
            "win_rate_percent": percentage
        }

    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)
    print("Time taken to play:", duration, "min\n")
    
    # Aggregate Reporting
    try:
         reporter = ReportGenerator()
         matchup_str = " vs ".join(matchup)
         reporter.save_aggregated_report(
             game_type=matchup_str,
             number_of_games=number_of_games,
             win_rates=win_rates,
             duration=duration,
             timestamp_start=time.ctime(start_time),
             timestamp_end=time.ctime(end_time)
         )
         print(f"Aggregate report saved for {matchup_str}")
    except Exception as e:
         print(f"Failed to save aggregate report: {e}")

    return

def assign_did_win(df):
    df['did_win'] = False
    games = df['game_id'].unique()
    for game in games:
        game_df = df[df['game_id'] == game]
        winning_indices = game_df[game_df['is_game_over']].index
        for idx in winning_indices:
            player_index = game_df.loc[idx, 'index_of_a_player']
            df.loc[(df['game_id'] == game) & (df['index_of_a_player'] == player_index), 'did_win'] = True
    return df

def save_to_csv(data, filename='uno_game.csv', folder='Uno/games_data'):
    if filename == 'uno_game.csv':
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{filename}"

    filepath = os.path.join(folder, filename)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(filepath):
        existing_df = pd.read_csv(filepath)
        combined_df = pd.concat([existing_df, data], ignore_index=True)
        combined_df.to_csv(filepath, index=False)
    else:
        data.to_csv(filepath, index=False)
    return filename

def open_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

def main():
    config = open_config()
    print("Initializing bot games")
    print("Pick '1' to make basic bots play against each other")
    print("Pick '2' to make C4.5Bot play against all basic bots")
    print("Pick '3' to make MCTS play against all basic bots")
    print("Pick '4' to make MCTS play against C4.5 bot")
    print("Pick '5' to make Random Forest (Bagging) play against all basic bots")
    x = input()

    print("How many games would you like each bot to play?")
    number_of_games = int(input())

    print(f"How many processes would you like to use? (Default: 5 | Max: {cpu_count()})")
    num_of_processes = int(input())
    
    matchups = []
    if x == "1":
        matchups = [
            # ["RandomBot", "AgressiveBot"],
            ["RandomBot", "BasicLogicBot"],
            ["AgressiveBot", "BasicLogicBot"]
        ]
    elif x == "2":
        matchups = [
            ["C4_5Bot", "AgressiveBot"],
            ["RandomBot", "C4_5Bot"],
            ["C4_5Bot", "BasicLogicBot"]
        ]
    elif x == "3":
        matchups = [
            ["MCTSBot", "AgressiveBot"],
            ["RandomBot", "MCTSBot"],
            ["MCTSBot", "BasicLogicBot"]
        ]
    elif x == "4":
        matchups = [
            ["MCTSBot", "C4_5Bot"]
        ]
    elif x == "5":
        matchups = [
            ["C4_5BaggingBot", "AgressiveBot"],
            ["RandomBot", "C4_5BaggingBot"],
            ["C4_5BaggingBot", "BasicLogicBot"]
        ]

    if number_of_games is None:
        number_of_games = config["main"]["number_of_games"]

    print(f"Games started at: {time.ctime(time.time())}")
    start_time = time.time()
    for matchup in matchups:
        start_many_games(matchup, number_of_games, num_of_processes)

    print(f"All {number_of_games * len(matchups):_} games played in ", round((time.time() - start_time) / 60, 2),
          "minutes\n")
    print(f"Games ended at: {time.ctime(time.time())}")


if __name__ == "__main__":
    main()
