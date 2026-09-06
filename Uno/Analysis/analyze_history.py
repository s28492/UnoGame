import os
import pandas as pd
import glob
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def load_all_game_data(data_folder='Uno/games_data'):
    """Loads all CSV files from the data folder into a single DataFrame."""
    all_files = glob.glob(os.path.join(data_folder, "*.csv"))
    
    if not all_files:
        console.print(f"[red]No CSV files found in {data_folder}[/red]")
        return pd.DataFrame()

    console.print(f"[green]Found {len(all_files)} files. Loading...[/green]")
    
    df_list = []
    for filename in track(all_files, description="Reading CSVs..."):
        try:
            df = pd.read_csv(filename)
            df_list.append(df)
        except Exception as e:
            console.print(f"[yellow]Skipping {filename}: {e}[/yellow]")

    if not df_list:
        return pd.DataFrame()

    full_df = pd.concat(df_list, ignore_index=True)
    return full_df

def analyze_win_rates(df):
    """Calculates overall win rates for each bot type."""
    # Filter for rows where the game ended for that player's perspective
    # 'did_win' is already calculated per player in main.py
    
    # We want to count unique games won per bot type.
    # Group by player_instance and calculate mean of did_win? 
    # Not exactly, because we need to know how many games they PLAYED.
    
    # Each row is a turn. 'is_game_over' marks the end.
    # We should look at unique (game_id, index_of_a_player) to count games played.
    
    # But wait, did_win is true for all rows of the winner in provided main.py?
    # Let's check main.py assign_did_win:
    # df.loc[(df['game_id'] == game) & (df['index_of_a_player'] == player_index), 'did_win'] = True
    # Yes, it propagates True to all rows of the winner.
    
    # So we can just group by game_id and take one row per player-game combo.
    # Actually, simpler: 
    # 1. Get unique games participations: (game_id, player_instance, did_win)
    
    games_participants = df[['game_id', 'player_instance', 'did_win']].drop_duplicates()
    
    stats = {}
    
    for bot_type in games_participants['player_instance'].unique():
        bot_games = games_participants[games_participants['player_instance'] == bot_type]
        games_played = len(bot_games)
        games_won = len(bot_games[bot_games['did_win'] == True])
        win_rate = (games_won / games_played * 100) if games_played > 0 else 0
        
        stats[bot_type] = {
            "played": games_played,
            "won": games_won,
            "win_rate": round(win_rate, 2)
        }
        
    return stats

def analyze_game_lengths(df):
    """Calculates average turns per game."""
    # Group by game_id and get max 'round'
    game_lengths = df.groupby('game_id')['round'].max()
    
    return {
        "avg_turns": round(game_lengths.mean(), 2),
        "min_turns": int(game_lengths.min()),
        "max_turns": int(game_lengths.max()),
        "total_games_analyzed": len(game_lengths)
    }

def analyze_matchups(df):
    """Calculates win rates for specific matchups (e.g., AgressiveBot vs RandomBot)."""
    console.print("[yellow]Analyzing matchups... (this might take a moment)[/yellow]")
    
    # 1. Get unique game participants info
    # We need: game_id, player_idx, bot_type, did_win
    # Note: 'index_of_a_player' is the column name in the CSV
    participants = df[['game_id', 'index_of_a_player', 'player_instance', 'did_win']].drop_duplicates()
    
    # 2. Pivot to get one row per game: game_id | 0_bot | 1_bot
    # We assume 2 players per game as per thesis constraints
    pivoted = participants.pivot(index='game_id', columns='index_of_a_player', values='player_instance')
    
    # Handle cases where maybe a game didn't have 2 players or data is weird
    pivoted = pivoted.dropna()
    pivoted.columns = ['player_0', 'player_1']
    
    # 3. Get the winner for each game
    winners = participants[participants['did_win'] == True].set_index('game_id')['player_instance']
    
    # 4. Join
    matchup_df = pivoted.join(winners.rename('winner'), how='inner')
    
    # 5. Create normalized matchup key (alphabetical order)
    # This ensures "Random vs Aggressive" and "Aggressive vs Random" are grouped together
    matchup_df['matchup'] = matchup_df.apply(lambda row: " vs ".join(sorted([row['player_0'], row['player_1']])), axis=1)
    
    # 6. Group and aggregate
    stats = {}
    
    grouped = matchup_df.groupby('matchup')
    
    for matchup_name, group in grouped:
        total_games = len(group)
        
        # Get counts of wins per bot in this matchup
        win_counts = group['winner'].value_counts()
        
        matchup_stats = {
            "total_games": total_games,
            "details": {}
        }
        
        # Determine the two bots involved from the matchup name string is risky if names have " vs ", 
        # but better to look at the group's unique values or just the win_counts keys.
        # But even better: we know the 2 bots from the matchup key if we split it, 
        # OR we just iterate over the bots that actually played
        
        bots_involved = set(matchup_name.split(" vs "))
        
        for bot in bots_involved:
            wins = win_counts.get(bot, 0)
            win_rate = (wins / total_games * 100)
            matchup_stats["details"][bot] = {
                "wins": int(wins),
                "win_rate": round(win_rate, 2)
            }
            
        stats[matchup_name] = matchup_stats
        
    return stats

def analyze_starting_advantage(df):
    """Checks if starting player wins more often."""
    # We need to link 'did_win' with 'index_of_a_player'.
    games_winners = df[df['did_win'] == True][['game_id', 'index_of_a_player']].drop_duplicates()
    
    win_counts = games_winners['index_of_a_player'].value_counts().to_dict()
    total_wins = sum(win_counts.values())
    
    advantage_stats = {}
    for idx, count in win_counts.items():
        advantage_stats[f"Player_{idx}"] = {
            "wins": count,
            "percentage": round((count / total_wins * 100), 2) if total_wins > 0 else 0
        }
        
    return advantage_stats

def save_analysis_report(stats, output_file="Reports/historical_analysis.json"):
    """Saves the comprehensive analysis to a JSON file."""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = {
        "timestamp": timestamp,
        "analysis": stats
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)
    
    console.print(f"[bold green]Analysis saved to {output_file}[/bold green]")

def print_table(title, data, headers=["Bot Type", "Played", "Won", "Win Rate (%)"]):
    table = Table(title=title)
    for h in headers:
        table.add_column(h)
        
    for key, val in data.items():
        if isinstance(val, dict) and "played" in val: # Global stats
            table.add_row(
                key, 
                str(val['played']), 
                str(val['won']), 
                f"{val['win_rate']}%"
            )
        elif "percentage" in val: # Advantage stats
             table.add_row(key, "-", str(val['wins']), f"{val['percentage']}%")
             
    console.print(table)

def print_matchup_table(stats):
    table = Table(title="Matchup Analysis")
    table.add_column("Matchup")
    table.add_column("Total Games")
    table.add_column("Result")
    
    for matchup, data in stats.items():
        details = []
        for bot, res in data['details'].items():
            details.append(f"{bot}: {res['win_rate']}% ({res['wins']})")
        
        table.add_row(
            matchup,
            str(data['total_games']),
            " | ".join(details)
        )
    console.print(table)

def main():
    console.rule("[bold blue]Uno Historical Data Analysis[/bold blue]")
    
    # 1. Load Data
    full_df = load_all_game_data()
    if full_df.empty:
        return

    # 2. Analyze Win Rates (Global)
    win_stats = analyze_win_rates(full_df)
    print_table("Global Bot Performance", win_stats)
    
    # 3. Analyze Matchups (New)
    matchup_stats = analyze_matchups(full_df)
    print_matchup_table(matchup_stats)

    # 4. Analyze Lengths
    length_stats = analyze_game_lengths(full_df)
    console.print(f"\n[bold]Game Length Stats (Turns):[/bold]")
    console.print(length_stats)

    # 5. Analyze Starting Advantage
    advantage_stats = analyze_starting_advantage(full_df)
    print_table("Starting Position Advantage", advantage_stats, headers=["Player Index", "-", "Wins", "Win Percentage"])

    # 6. Compile and Save
    full_report = {
        "bot_performance_global": win_stats,
        "matchup_performance": matchup_stats,
        "game_length_stats": length_stats,
        "starting_advantage": advantage_stats,
        "total_records_processed": len(full_df)
    }
    
    save_analysis_report(full_report)

if __name__ == "__main__":
    main()
