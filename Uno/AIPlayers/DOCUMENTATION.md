# Dokumentacja Techniczna: Agenci AI i Naiwny Klasyfikator Bayesowski (`Uno/AIPlayers`)

## 1. Architektura Bazowa Agentów Sztucznej Inteligencji (`BaseAIBot.py`)

Wszyscy zaawansowani agenci uczenia maszynowego dziedziczą po klasie `BaseAIBot`, która integruje logikę gracza z silnikiem pozyskiwania cech w czasie rzeczywistym.

- **`create_row(dict)`:** Przekształca słownik cech pozyskany z `GameState` w jednoliniową ramkę danych Pandas (`current_row`).
- **`current_data`:** Agreguje sekwencję historyczną tur agenta w celach dalszej analizy lub douczenia online.

---

## 2. Naiwny Klasyfikator Bayesowski (`NaiveBayesianBot.py`)

`NaiveBayesianBot` podejmuje decyzje decyzyjne na podstawie probabilistycznego wyliczenia prawdopodobieństwa a posteriori zagrania danej karty.

### 2.1. Sformułowanie Matematyczne
Zgodnie z Twierdzeniem Bayesa, prawdopodobieństwo, że optymalnym ruchem przy zaobserwowanym wektorze cech $x = (x_1, x_2, \dots, x_n)$ jest zagranie akcji $a \in \mathcal{A}$, wynosi:

$$P(a \mid x) = \frac{P(a) \cdot P(x \mid a)}{P(x)}$$

Mianownik $P(x)$ jest stały dla wszystkich rozważanych akcji w danej turze, co pozwala na uproszczenie do zagadnienia optymalizacyjnego:

$$a^* = \arg\max_{a \in \text{Valid}(s)} P(a \mid x) = \arg\max_{a \in \text{Valid}(s)} P(a) \cdot P(x \mid a)$$

---

### 2.2. Założenie Warunkowej Niezależności Cech (*Naive Assumption*)
Naiwny klasyfikator bayesowski przyjmuje kategoryczne założenie, że wszystkie cechy $x_1, x_2, \dots, x_n$ są od siebie warunkowo niezależne przy podanej klasie $a$:

$$P(x \mid a) = \prod_{i=1}^{n} P(x_i \mid a)$$

Stąd ostateczna reguła decyzyjna bota przyjmuje postać:

$$a^* = \arg\max_{a \in \text{Valid}(s)} \left( P(a) \prod_{i=1}^{n} P(x_i \mid a) \right)$$

gdzie:
- $P(a) = \frac{|D_a|}{|D|}$ – prawdopodobieństwo aprioryczne zagrania karty $a$ w zbiorze treningowym $D$.
- $P(x_i \mid a) = \frac{\sum \mathbb{I}(X_i = x_i \land Y = a)}{|D_a|}$ – prawdopodobieństwo warunkowe wystąpienia cechy $x_i$ przy zagraniu karty $a$.

---

### 2.3. Akceleracja Numeryczna JIT z Numba (`calculate_naive_bayes`)

Obliczanie iloczynów prawdopodobieństw w czasie rzeczywistym dla każdej tury zostało zoptymalizowane numerycznie z wykorzystaniem kompilacji JIT biblioteki **Numba** (`@njit(nogil=True)`):

```python
@njit(nogil=True)
def calculate_naive_bayes(numpy_current_row: np.array, numpy_data: np.array, probability_of_target_attribute: float):
    num_of_samples = numpy_data.shape[0]
    num_of_features = numpy_data.shape[1] - 1
    data_to_multiply = np.zeros(num_of_features)

    for i in range(num_of_features):
        occurrences = numpy_data[:, i] == numpy_current_row[0][i]
        number_of_occurrences = np.sum(occurrences)
        # Laplace smoothing w przypadku braku obserwacji
        partial_probability_value = number_of_occurrences / num_of_samples if number_of_occurrences != 0 else 1 / np.sum(np.unique(numpy_data[:, i]))
        data_to_multiply[i] = partial_probability_value

    final_probability = np.prod(data_to_multiply) * probability_of_target_attribute
    return final_probability
```

- **Wygładzanie Laplace'a (*Laplace Smoothing*):** W przypadku braku wystąpienia danej wartości cechy w zbiorze treningowym ($n_i = 0$), algorytm stosuje wygładzanie zapobiegające zerowaniu całego iloczynu prawdopodobieństw.

---

## 3. Teoretyczna Analiza Porażki Założenia Niezależności w Uno

Wykorzystanie Naiwnego Klasyfikatora Bayesowskiego w środowisku Uno reprezentuje teoretyczny konflikt założeń modelowych z rzeczywistością gry:

1. **Silna Korelacja Cech (Violation of Independence):** W Uno cechy takie jak `num_red`, `num_colors_in_hand`, `top_card` i `num_playable_cards` są ścisłe powiązane funkcjonalnie. Na przykład:
   $$P(\text{num\_playable\_cards} > 0 \mid \text{num\_red} = 5, \text{top\_card} = \text{"Red 3"}) = 1$$
   Iloczynowe traktowanie tych zmiennych sztucznie potęguje lub zaniża szacowane prawdopodobieństwa.
2. **Degeneracja w Stochastyczności:** Ze względu na niepełną informację i stochastyczne dociąganie kart ze stosu, statystyczna rozkład cech z przeszłych gier nie odzwierciedla wartości taktycznej karty w obecnym układzie stołu.
