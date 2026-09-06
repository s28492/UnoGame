# Moduł `Uno/players` – Boty Heurystyczne i Regułowe

Katalog zawiera implementacje podstawowych graczy (botów heurystycznych) wykorzystywanych zarówno jako rywale referencyjni (baselines), jak i do generowania danych treningowych.

## 📄 Zawartość Modułu

- **`Player.py`** – Główna klasa bazowa definiująca interfejs gracza (posiadana ręka, wybór karty, zmiana koloru).
- **`Bot.py`** – Ogólna klasa rozszerzająca `Player` o logikę automatycznego podejmowania decyzji.
- **`RandomBot.py`** – Bot podejmujący całkowicie losowe (lecz legalne) decyzje spośród dostępnych kart na ręce.
- **`BasicLogicBot.py`** – Bot stosujący podstawową heurystykę: dopasowywanie wartości/kolorów oraz wybór dominującego koloru na ręce.
- **`BLBUpgradedColorChoosingBot.py`** – Udoskonalona wersja `BasicLogicBot` z bardziej zaawansowaną strategią wyboru optymalnego koloru.
- **`AgressiveBot.py`** – Bot heurystyczny priorytetyzujący karanie przeciwnika kartami akcji (+2, +4) i pozbywanie się kart wysokopunktowych.
