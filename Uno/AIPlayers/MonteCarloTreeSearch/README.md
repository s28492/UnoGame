# Moduł `Uno/AIPlayers/MonteCarloTreeSearch` – Algorytm MCTS

Moduł zawiera dedykowaną implementację algorytmu **Przeszukiwania Drzewa Gry metodą Monte Carlo (Monte Carlo Tree Search)** dostosowaną do stochastycznego środowiska gry Uno z niepełną informacją.

## 📄 Zawartość Modułu

- **`MCTSBot.py`** – Interfejs gracza MCTS realizujący cztery fazy algorytmu: *Selection*, *Expansion*, *Simulation (Rollout)* oraz *Backpropagation*.
- **`Node.py`** – Klasa węzła w drzewie poszukiwań MCTS przechowująca statystyki wygranych/rozgrywek oraz powiązane akcje.
- **`Simulation.py`** – Moduł odpowiedzialny za wykonywanie szybkich losowych lub heurystycznych symulacji rozgrywki (symulowany roll-out).
