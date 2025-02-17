import os
import time
from datetime import datetime
from Uno.players.RandomBot import BotRandom
from Uno.players.BasicLogicBot import BasicLogicBot
from Uno.players.AgressiveBot import AgressiveBot
from Uno.players.BLBUpgradedColorChoosingBot import BLBUpgradedColorChoosing
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.AIPlayers.NaiveBayesianBot import NaiveBayesianBot
from Uno.DecisionTrees.C4_5Tree import load_tree as load_C4_5
from Uno.DecisionTrees.C4_5Tree import C4_5Tree
from Uno.AIPlayers.C4_5BaggingEnsemble import C4_5BaggingEnsebleBot
from Uno.game.Game import Game
from rich.console import Console
from multiprocessing import Pool, Manager, cpu_count
import random
import pandas as pd
from collections import Counter

console = Console()
bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]

pd.set_option('future.no_silent_downcasting', True)
def create_game_with_players(*players) -> Game:
    """returns game with initialized starting state"""
    return Game(players)

def create_instances(bots, location=None):
    names = bot_names.copy()
    random.shuffle(names)
    instances_to_return = []
    for bot in bots:
        if bot == "BasicLogicBot":
            instances_to_return.append(BasicLogicBot("BasicLogicBot"))
        elif bot == "AgressiveBot":
            instances_to_return.append(AgressiveBot("AgressiveBot"))
        elif bot == "RandomBot":
            instances_to_return.append(BotRandom("BotRandom"))
        elif bot == "C4_5Bot":
            name = "C4_5Bot"
            if location is not None:
                tree = load_C4_5(location)
            else:
                tree = load_C4_5("Uno/DecisionTrees/Models/20250111_1355_3GB_Dataset_C4_5Tree_tree_d100_mvl200_gr0_03.pkl")
            instances_to_return.append(C4_5Bot(name, tree_instance=tree))
        elif bot == "NaiveBayesianBot1":
            name = "NaiveBayesianBot1"
            bot: NaiveBayesianBot = NaiveBayesianBot(name, data=data.copy(), labels_to_decode=label)
            instances_to_return.append(bot)
        elif bot == "NaiveBayesianBot2":
            name = "NaiveBayesianBot2"
            bot: NaiveBayesianBot = NaiveBayesianBot(name, data=data2.copy(), labels_to_decode=label2)
            instances_to_return.append(bot)
        elif bot == "BaggingBot":
            name = "BaggingBot"
            bot: C4_5BaggingEnsebleBot = C4_5BaggingEnsebleBot(name, "Uno/DecisionTrees/Models")
            instances_to_return.append(bot)
        elif bot == "MCTSBot1":
            name = "MCTSBot1"
            bot: MCTSBot = MCTSBot(name, num_of_simulations=200, c_param=1.85)
            instances_to_return.append(bot)
        elif bot == "MCTSBot2":
            name = "MCTSBot2"
            bot: MCTSBot = MCTSBot(name, num_of_simulations=10_000, c_param=1.95)
            instances_to_return.append(bot)
        elif bot == "MCTSBot3":
            name = "MCTSBot3"
            bot: MCTSBot = MCTSBot(name, num_of_simulations=10_000, c_param=1.9)
            instances_to_return.append(bot)
        else:
            instances_to_return.append(BLBUpgradedColorChoosing("BLBUpgradedColorChoosing"))
        
    return instances_to_return

def play_game(matchup, location=None):
    bots = create_instances(matchup, location)
    game = start_2_bot_games(bots)
    bots.clear()
    current_game_data = assign_did_win(pd.DataFrame(game[0]))
    winner = game[1].name
    return current_game_data, winner

def start_2_bot_games(matchup):
    game = create_game_with_players(*matchup)
    return game.play()

def start_many_games(matchup, number_of_games=1000, location=None):
    manager = Manager()
    games_data = manager.list()  # Use Manager list
    who_won = manager.list()

    def collect_results(result):
        current_game_data, winner = result
        games_data.append(current_game_data)
        who_won.append(winner)

    start_time = time.time()
    num_of_processes = cpu_count() - 1 if cpu_count() > 1 else 1
    print("Games starting...")
    with Pool(processes=num_of_processes-2) as pool:
        results = [pool.apply_async(play_game, (matchup,location,), callback=collect_results) for _ in range(number_of_games)]
        pool.close()
        pool.join()

    df = pd.concat(list(games_data))
    file_name = save_to_csv(df, 'uno_game.csv')
    print(f"Saved to file '{file_name}'...")

    win_count = Counter(who_won)
    for bot_name, count in win_count.items():
        print(f"{bot_name}: {count} wins, {round((count / number_of_games) * 100, 2)}%")

    end_time = time.time()
    print("Time taken to play:", round((end_time - start_time) / 60, 2), "min\n")
    return


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

if __name__ == "__main__":
    print("Initializing bot games")
    print("Pick '1' to make basic bots play against each other")
    print("Pick '2' to make C4.5Bot play against all basic bots")
    x = input()
    location = None

    print("How many games would you like each bot to play? Recomended  1_000 for C4.5Bot")
    number_of_games = int(input())
    if x == "1":
        matchups = [
            ["RandomBot", "AgressiveBot"],
            ["RandomBot", "BasicLogicBot"],
            ["AgressiveBot", "BasicLogicBot"]
        ]
    elif x == "2":
        matchups = [
            ["C4_5Bot", "AgressiveBot"],
            ["RandomBot", "C4_5Bot"],
            ["C4_5Bot", "BasicLogicBot"]
        ]
        print("Input location of trained tree model")
        location = input()
    if number_of_games is None:
        number_of_games = 1_000
    for _ in range(1):
        start_time = time.time()
        for matchup in matchups:
            start_many_games(matchup, number_of_games, location)

        print(f"All {number_of_games*len(matchups):_} games played in ", round((time.time() - start_time)/60, 2), "minutes\n")
        print(f"Games ended at: {time.ctime(time.time())}")
