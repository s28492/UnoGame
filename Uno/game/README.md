# Moduł `Uno/game` – Silnik Gry i Stan Rozgrywki

Moduł odpowiada za pełne odwzorowanie mechaniki gry w Uno, zarządzanie talią kart, weryfikację zasad oraz reprezentację stanu gry dla agentów AI.

## 📄 Zawartość Modułu

- **`Card.py`** – Reprezentacja pojedynczej karty Uno (kolor, wartość/figura, karty specjalne +2, +4, Zmiana Kierunku, Stop, Dzikie Karty).
- **`Deck.py`** – Klasa zarządzająca talią, przetasowywaniem, dobieraniem kart oraz stosami kart zagranych i zakrytych.
- **`Game.py`** – Główny silnik sterujący przebiegiem rozgrywki: pętla tury, zagrywanie kart, nakładanie efektów kar, rozstrzyganie zwycięzcy.
- **`GameState.py`** – Obiekt reprezentujący pełny stan gry w danej turze (w tym wektoryzacja stanu na potrzeby modeli ML/AI).
