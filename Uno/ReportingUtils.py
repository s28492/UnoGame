
import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="Reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save_game_report(self, game_id, winner_name, duration, bots_config):
        report = {
            "game_id": game_id,
            "timestamp": datetime.now().isoformat(),
            "winner": winner_name,
            "duration_minutes": duration,
            "bots": bots_config
        }
        
        filename = f"game_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{game_id}.json"
        with open(os.path.join(self.output_dir, filename), "w") as f:
            json.dump(report, f, indent=4)
            
    def save_training_report(self, model_name, config, notes):
        report = {
            "model_name": model_name,
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "notes": notes
        }
        filename = f"training_report_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(self.output_dir, filename), "w") as f:
            json.dump(report, f, indent=4)

    def save_aggregated_report(self, game_type, number_of_games, win_rates, duration, timestamp_start, timestamp_end):
        report = {
            "game_type": game_type,
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
            "number_of_games": number_of_games,
            "duration_minutes": duration,
            "win_rates": win_rates
        }
        
        filename = "aggregated_reports.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        # If for some reason it's not a list, wrap it or start new
                        data = [data]
            except json.JSONDecodeError:
                # File might be empty or corrupted
                data = []
        
        data.append(report)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
