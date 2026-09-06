'''
@author Cyprian Szewczak s28492

'''
import time

from Uno.players.Player import Player
from Uno.players.Bot import Bot
from Uno.players.RandomBot import BotRandom
from Uno.AIPlayers.C4_5Bot import C4_5Bot
from Uno.AIPlayers.MonteCarloTreeSearch.MCTSBot import MCTSBot
# from Uno.AIPlayers.DQLBot.DQLBot import DQLBot


from Uno.game.Game import Game
from rich.console import Console
import random

from Uno.ReportingUtils import ReportGenerator

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
    reporter = ReportGenerator()
    
    console.print("\n[bold magenta]Welcome to UNO game![/bold magenta]",justify="center", end="\n\n")
    console.print("1. Play with other humans.", justify="center")
    console.print("2. Watch bots playing with each other.", justify="center")
    console.print("3. Play with humans and bots.", justify="center")
    console.print(
        "4. Play with AI (C4.5 model).", justify="center"
    )
    console.print(
        "5. Play with AI (MCTS model).", justify="center", end="\n\n"
    )


    choice = console.input("[bold green]Pick an option (1-4): [/bold green]")

    human_player_name = console.input("[bold green]Now pick your name [/bold green]")

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
        bots = [ Player(human_player_name), C4_5Bot(bot_names.pop())]
        random.shuffle(bots)
        game = create_game_with_players(bots)
    elif choice == "5":
        bots = [ Player(human_player_name), MCTSBot(bot_names.pop(), 50_000, 1.9)]
        random.shuffle(bots)
        game = create_game_with_players(bots)
    else:
        console.print("[bold red]Wrong choice![/bold red]\nLet's try again...\n")
        return main()
        
    if game:
        start_time = time.time()
        _, winner = game.play()
        game_duration = (time.time() - start_time) / 60
        
        console.print(f"[bold]And the winner is [yellow] {winner}[/yellow][/bold]")
        
        # Report Generation
        bots_config = {}

        current_players = []
        if hasattr(game, 'players'):
            current_players = game.players
        elif hasattr(game, 'get_players'):
             current_players = game.get_players()
        else:
             pass

        
        for player in (game.players if hasattr(game, 'players') else []):
             if hasattr(player, 'get_config'):
                 bots_config[player.get_name()] = player.get_config()
             else:
                 bots_config[player.get_name()] = str(player)

        reporter.save_game_report(
            game_id=f"interactive_{int(time.time())}",
            winner_name=str(winner),
            duration=game_duration,
            bots_config=bots_config
        )


def start_2_bot_games():
    bot_names = ["Beta", "Andromeda", "Sora", "Korgi", "Ultron", "Vien", "Polak", "Ziemniak", "Hal 9000", "Agent Smith"]
    random.shuffle(bot_names)
    bots = []
    game = None
    reporter = ReportGenerator()

    num_bots = 2
    bots = [BotRandom(bot_names.pop()) for _ in range(num_bots if num_bots < 11 else 10)]
    game = create_game_with_players(bots)
    start_time = time.time()
    _, winner = game.play()
    game_duration = (time.time() - start_time) / 60
    
    bots_config = {p.get_name(): p.get_config() for p in bots}
    reporter.save_game_report(
        game_id=f"bot2bot_{int(time.time())}",
        winner_name=str(winner),
        duration=game_duration,
        bots_config=bots_config
    )

def start_many_games():
    number_of_games = 10
    start_time = time.time()
    for i in range(number_of_games):
        start_2_bot_games()
    end_time = time.time()
    print(f"{number_of_games} games played in: {end_time-start_time}")

if __name__ == "__main__":
    main()