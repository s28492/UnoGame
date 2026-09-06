import time

from Uno.game.Game import Game
import yaml
from src.utils import open_config
from Uno.DecisionTrees.C4_5Tree import C4_5Tree, load_tree
from Uno.players.AgressiveBot import AgressiveBot
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.AIPlayers.C4_5BaggingEnsemble import C4_5BaggingEnsebleBot
from Uno.AIPlayers.MonteCarloTreeSearch.MCTSBot import MCTSBot
# from Uno.AIPlayers.DQLBot.DQLBot import DQLBot


from Uno.ReportingUtils import ReportGenerator

# tree = load_tree("/mnt/xD/Projekty/Python/NewUnoGame/UnoGame/Uno/DecisionTrees/20240801_2159_improved_7_nodes_deep_decoded_target_values_tree.pkl")
# bagging_bot = C4_5BaggingEnsebleBot("Bagging Bot", "Uno/DecisionTrees/Models")
# ai_bot = ID3Bot(name="AI Bot", tree_instance=tree)

configs = open_config()
mcts_name = configs["mcts"]["name"]
mcts_num_of_simulations = configs["mcts"]["number_of_games"]
mcts_c_param = configs["mcts"]["c_parameter"]

reporter = ReportGenerator()

start_time = time.time()
for i in range(1_000):
    game_start = time.time()
    print(f"Starting game {i+1}")
    # bot1 = AgressiveBot("Aggressive")
    bot1: C4_5Bot = C4_5Bot("C4_5Bot")
    # bot2: DQLBot = DQLBot("DQLBot")
    bot2: MCTSBot = MCTSBot("MCTSBot", num_of_simulations=mcts_num_of_simulations, c_param=mcts_c_param)
    
    game = Game([bot1, bot2])
    _, winner = game.play()
    
    game_duration = (time.time() - game_start)
    print(winner, f" time: {game_duration}")
    
    # Generate Report
    bots_config = {
        bot1.get_name(): bot1.get_config(),
        bot2.get_name(): bot2.get_config()
    }
    
    reporter.save_game_report(
        game_id=f"game_{i+1}",
        winner_name=str(winner),
        duration=game_duration,
        bots_config=bots_config
    )

print("Time taken: ", (time.time() - start_time))