import json
import math
from scipy import stats
import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()

def load_report(filepath="Reports/historical_analysis.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def calculate_confidence_interval(wins, n, confidence=0.95):
    """
    Calculates the Wilson Score Interval for a binomial proportion.
    """
    if n == 0: return (0, 0)
    
    p = wins / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    
    # Wilson score interval formula
    denominator = 1 + z**2/n
    center_adjusted_probability = p + z**2 / (2*n)
    adjusted_standard_deviation = z * math.sqrt((p*(1 - p) + z**2 / (4*n)) / n)
    
    lower_bound = (center_adjusted_probability - adjusted_standard_deviation) / denominator
    upper_bound = (center_adjusted_probability + adjusted_standard_deviation) / denominator
    
    return (lower_bound * 100, upper_bound * 100)

def chisquare_test(wins_A, total_A, wins_B, total_B):
    """
    Performs a Chi-Square test of independence to see if the win rates are significantly different.
    Null Hypothesis: Win rates are the same.
    """
    # Contingency table:
    #       | Win | Loss
    # Bot A | wA  | tA - wA
    # Bot B | wB  | tB - wB
    
    obs = np.array([
        [wins_A, total_A - wins_A],
        [wins_B, total_B - wins_B]
    ])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(obs)
    return p_value

def analyze_matchup_significance(report):
    console.print("[bold]Statistical Significance Analysis (p < 0.05)[/bold]")
    
    matchups = report['analysis']['matchup_performance']
    table = Table(title="Matchup Significance Tests")
    table.add_column("Matchup")
    table.add_column("Bot A (Win Rate)")
    table.add_column("Bot B (Win Rate)")
    table.add_column("P-Value")
    table.add_column("Significant?")
    
    for matchup_name, data in matchups.items():
        details = data['details']
        bots = list(details.keys())
        if len(bots) != 2: continue
        
        botA = bots[0]
        botB = bots[1]
        
        winsA = details[botA]['wins']
        total = data['total_games'] # Both played same amount in a matchup
        # Wait, usually total_games is total games played.
        # Win rate is wins / total_games.
        # But here total_games is for the matchup. 
        # So botA played 'total' games. botB played 'total' games.
        # Actually corresponding wins sum to total (ignoring draws).
        # Assuming draws are negligible or counted as not-win.
        # Let's verify sum of wins.
        
        winsB = details[botB]['wins']
        draws = total - (winsA + winsB)
        
        # We compare Win Rate of A vs Win Rate of B?
        # Actually in a zero-sum 1v1 game, checking if WinRate != 50% is enough.
        # Or comparing proportions.
        
        # Let's test if the distribution of wins [A, B] (ignoring draws) differs from [0.5, 0.5]
        # Or simply Chi-square goodness of fit.
        
        valid_games = winsA + winsB
        if valid_games == 0: continue
        
        res = stats.chisquare([winsA, winsB])
        p_val = res.pvalue
        
        is_sig = "[green]YES[/green]" if p_val < 0.05 else "[red]NO[/red]"
        
        table.add_row(
            matchup_name,
            f"{botA} ({details[botA]['win_rate']}%)",
            f"{botB} ({details[botB]['win_rate']}%)",
            f"{p_val:.4e}",
            is_sig
        )
    
    console.print(table)
    return

def analyze_global_confidence(report):
    console.print("\n[bold]95% Confidence Intervals for Global Win Rates[/bold]")
    
    global_stats = report['analysis']['bot_performance_global']
    table = Table(title="Global Performance Confidence")
    table.add_column("Bot")
    table.add_column("Win Rate")
    table.add_column("95% CI")
    
    for bot, data in global_stats.items():
        wins = data['won']
        total = data['played']
        
        lower, upper = calculate_confidence_interval(wins, total)
        
        table.add_row(
            bot,
            f"{data['win_rate']}%",
            f"[{lower:.2f}%, {upper:.2f}%]"
        )
    
    console.print(table)

def main():
    try:
        report = load_report()
    except FileNotFoundError:
        console.print("[red]Report file not found![/red]")
        return

    analyze_global_confidence(report)
    analyze_matchup_significance(report)

if __name__ == "__main__":
    main()
