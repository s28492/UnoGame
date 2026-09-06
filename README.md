# UnoGame – Platforma Badawcza i Silnik Symulacji Uno AI

Projekt realizowany w ramach pracy inżynierskiej. System umożliwia symulowanie automatycznych rozgrywek 2-osobowych w grę Uno z udziałem botów regułowych, heurystycznych oraz zaawansowanych agentów opartych na uczeniu maszynowym.

## 🎯 Główne Cele Projektu
- **Implemetacja silnika gry Uno** zgodnego z oficjalnymi zasadami i architekturą zorientowaną na reprezentację stanów (`GameState`).
- **Ekstrakcja danych i telemetrii** z rozgrywek botów heurystycznych do uczenia nadzorowanego i z naśladownictwa (*Imitation Learning*).
- **Ewaluacja porównawcza** algorytmów klasycznych (C4.5, Naive Bayes), statystycznego przeszukiwania drzew (MCTS), uczenia ze wzmocnieniem (Q-Learning) oraz sieci neuronowych (PyTorch).
- **Analiza statystyczna** skuteczności i wskaźników wygranych (Win Rate) poszczególnych botów.

## 📂 Struktura Projektu

- **`Uno/`** – Rdzenny moduł Python zawierający silnik gry, graczy, agentów AI oraz moduły uczenia modeli.
- **`Reports/`** – Katalog na automatycznie generowane raporty z rozgrywek w formacie JSON oraz zagregowane dane statystyczne.
- **`src/`** – Pomocnicze funkcje narzędziowe i wsparcie systemowe.
- **`config.yml`** – Plik konfiguracyjny ścieżek modeli i parametrów symulacji.

## 🤖 Podsumowanie Dostępnych Botów

### Boty Heurystyczne / Regułowe
* **`RandomBot`**: Wybiera losową legalną kartę z ręki.
* **`BasicLogicBot`**: Zagra dopasowaną kartę priorytetyzując dopasowanie koloru/figury, wybiera najczęstszy kolor.
* **`AggressiveBot`**: Priorytetyzuje karty akcji (+2, +4, Zmiana Kierunku, Stop) oraz karty o wysokiej punktacji.

### Agenci Uczenia Maszynowego (AI)
* **`C4_5Bot` / `BaggingEnsemble`**: Klasyfikator drzew decyzyjnych (lub zespół drzew) przewidujący optymalne zagranie.
* **`NaiveBayesianBot`**: Naiwny klasyfikator bayesowski bazujący na statystykach stanu gry.
* **`SimpleNNBot`**: Sieć neuronowa wyszkolona metodą uczenia z naśladownictwa (*Imitation Learning*).
* **`MCTSBot`**: Przeszukiwanie drzewa gry metodą Monte Carlo symulujące przyszłe stany rozgrywki.

## 🛠 Uruchomienie

1. **Instalacja zależności:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Uruchomienie interfejsu konsolowego:**
   ```bash
   python -m Uno.main
   ```
