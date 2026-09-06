# Pakiet `Uno` – Główny Moduł Systemowy

Katalog `Uno` stanowi serce aplikacji i reprezentuje pakiet Python zawierający logiczną architekturę gry, implementacje graczy oraz algorytmy uczenia maszynowego.

## 📂 Podkatalogi i Moduły

- **`game/`** – Logika gry Uno (karty, talia, weryfikacja zasad, obsługa stanów `GameState`).
- **`players/`** – Klasa bazowa `Player` oraz boty heurystyczne/regułowe (`RandomBot`, `BasicLogicBot`, `AggressiveBot`).
- **`AIPlayers/`** – Klasa bazowa `BaseAIBot` oraz zaawansowani agenci AI (`C4_5Bot`, `NaiveBayesianBot`, `SimpleNNBot`, `MCTSBot`).
- **`DecisionTrees/`** – Implementacja algorytmów drzew decyzyjnych (ID3, C4.5, RandomForest) oraz skryptów trenujących.
- **`NeuralNetwork/`** – Modele sieci neuronowych w PyTorch oraz notebooki Jupyter do nauki z naśladownictwa.
- **`QLearning/`** – Moduł zorientowany na uczenie ze wzmocnieniem.
- **`Analysis/`** – Skrypty do analizy statycznej logów rozgrywek i przeprowadzania testów istotności statystycznej.
- **`games_data/`** – Surowe dane historyczne generowane podczas symulacji gier na potrzeby uczenia modeli.

## 📜 Główne Skrypty Wykonawcze

- **`main.py`** – Główny punkt wejścia CLI umożliwiający wybór trybu rozgrywki i konfigurację botów.
- **`play_game.py` / `run_game.py`** – Skrypty uruchamiające pętlę symulacji pojedynczych gier lub serii meczów.
- **`ReportingUtils.py`** – Moduł pomocniczy do rejestrowania metryk rozgrywki i zapisu raportów JSON.
