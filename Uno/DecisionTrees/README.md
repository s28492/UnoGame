# Moduł `Uno/DecisionTrees` – Drzewa Decyzyjne i Zespoły (Ensembles)

Katalog dedykowany tworzeniu, trenowaniu, ewaluacji i serializacji modeli opartych na drzewach decyzyjnych oraz lasach losowych.

## 📄 Zawartość Modułu

- **`C4_5Tree.py`** – Własna implementacja algorytmu C4.5 uwzględniająca podziały na podstawie współczynnika zysku informacji (*Gain Ratio*).
- **`ID3Tree.py`** – Implementacja algorytmu ID3 (Gain Information).
- **`BuildTree.py` / `ExpandTree.py`** – Skrypty pomocnicze do konstrukcji i rozbudowy struktur drzew.
- **`RandomForest.py` / `RF_Creator.py`** – Budowanie i ewaluacja klasyfikatorów typu Las Losowy (*Random Forest*).
- **`baggingCreator.py`** – Skrypty generujące modele zespołowe oparte na technice Baggingu.
- **`Models/`** – Zapisane wstępnie wytrenowane modele w formacie `.pkl`.
