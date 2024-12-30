from Uno.game.Game import Game
from Uno.DecisionTrees.C4_5Tree import C4_5Tree, load_tree
from Uno.players.AgressiveBot import AgressiveBot
from Uno.AIPlayers.ID3Bot import ID3Bot
from Uno.AIPlayers.C4_5BaggingEnsemble import C4_5BaggingEnsebleBot
from Uno.AIPlayers.MonteCarloTreeSearch.MCTSBot import MCTSBot


# tree = load_tree("Uno/DecisionTrees/Models/20241226_1957_3GB_Dataset_C4_5Tree_tree_d100_mvl200_gr0.03.pkl")
# bagging_bot = C4_5BaggingEnsebleBot("Bagging Bot", "Uno/DecisionTrees/Models")
# ai_bot = ID3Bot(name="AI Bot", tree_instance=tree)
for i in range(1):
    bot = AgressiveBot("Aggressive")
    mcts_bot: MCTSBot = MCTSBot("MCTSBot")
    game = Game([bot, mcts_bot])
    winner = game.play()
    print(winner[1])