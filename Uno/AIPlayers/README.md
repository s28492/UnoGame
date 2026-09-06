# Moduł `Uno/AIPlayers` – Zaawansowani Agenci AI

Katalog zawiera agenty sztucznej inteligencji, które podejmują decyzje w oparciu o wyliczenia algorytmiczne, przetestowane modele uczenia maszynowego lub symulacje drzew gry.

## 📄 Zawartość Modułu

- **`BaseAIBot.py`** – Klasa abstrakcyjna/bazowa dla wszystkich botów opartych na modelach sztucznej inteligencji.
- **`C4_5Bot.py`** – Bot wykorzystujący model pojedynczego drzewa decyzyjnego C4.5 do wyboru optymalnej akcji.
- **`C4_5BaggingEnsemble.py`** – Zespół klasyfikatorów (*Ensemble*) oparty na metodzie Baggingu dla drzew C4.5, poprawiający stabilność decyzji.
- **`NaiveBayesianBot.py`** – Bot decyzyjny oparty na Naiwnym Klasyfikatorze Bayesowskim.
- **`SimpleNNBot.py`** – Bot wykorzystujący model sieci neuronowej wyszkolony w procesie Uczenia z Naśladownictwa (*Imitation Learning*).
- **`QlearningBot.py`** – Agent uczący się strategii metodą Reinforcement Learning (Q-Learning).
- **`MonteCarloTreeSearch/`** – Podkatalog zawierający pełną implementację algorytmu przeszukiwania drzewa gry MCTS.
