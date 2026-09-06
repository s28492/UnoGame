# Dokumentacja Techniczna: Analiza Statystyczna i Ewaluacja (`Uno/Analysis`)

## 1. Ramy Metodologiczne Ewaluacji Badawczej

Katalog `Uno/Analysis` zawiera moduły analityczne odpowiedzialne za przetwarzanie zbiorów danych wygenerowanych w procesie masowych symulacji oraz przeprowadzanie formalnych weryfikacji statystycznych hipotez badawczych.

Pipeline analityczny:
1. **Generacja Telemetrii:** Rejestracja przebiegu rozgrywek w formacie CSV w katalogu `games_data/`.
2. **Agregacja i Podsumowanie (`analyze_history.py`):** Ekstrakcja kluczowych metryk (Win Rate, długość gier, mecze bezpśrednie, przewaga pierwszego gracza).
3. **Testowanie Hipotez (`statistical_tests.py`):** Wyliczenie przedziałów ufności oraz p-wartości (*p-values*) testów istotności.

---

## 2. Kluczowe Metryki Sukcesu i Zbiorcze Metody Agregacji

### 2.1. Wskaźnik Wygranych (Win Rate)
Proporcja wygranych meczów dla bota typu $B$ zdefiniowana jest jako:

$$\text{WinRate}(B) = \frac{\sum_{i=1}^{M_B} \mathbb{I}(\text{Winner}_i = B)}{M_B} \times 100\%$$

gdzie $M_B$ to całkowita liczba rozegranych przez tego bota meczów.

### 2.2. Długość Rozgrywki (Game Length Stats)
Średnia liczba tur $\bar{T}$ oraz wariancja długości gry:

$$\bar{T} = \frac{1}{M} \sum_{i=1}^{M} t_i, \quad \sigma_T^2 = \frac{1}{M-1} \sum_{i=1}^{M} (t_i - \bar{T})^2$$

---

## 3. Formalne Testy Statystyczne (`statistical_tests.py`)

Aby wykluczyć wływ przypadku i szumu stochastycznego w dociąganiu kart, wygenerowane wyniki są poddawane rygorystycznym testom matematycznym.

### 3.1. Przedział Ufności Wilsona (Wilson Score Interval)
W przeciwieństwie do zwykłego przedziału Waldnera, **przedział score Wilsona** nie ulega zniekształceniu przy skrajnych wartościach proporcji dwumianowej ($p \approx 0$ lub $p \approx 1$):

$$\text{CI}_{95\%} = \frac{p + \frac{z^2}{2n} \pm z \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

dla poziomu ufności $95\%$ wartość krytyczna rozkładu normalnego wynosi $z = 1.960$.

---

### 3.2. Test Istotności Chi-Kwadrat ($\chi^2$ Test)
W celu weryfikacji hipotezy zerowej $H_0$: *"Skuteczność bota A oraz bota B w bezpośrednim pojedynku nie różni się w sposób istotny statystycznie"*, obliczana jest statystyka Chi-kwadrat dla tablicy dwudzielczej 2x2:

$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$

gdzie $O_i$ to obserwowana liczba wygranych, a $E_i$ to oczekiwana liczba wygranych przy założeniu równej szansy ($50\%$).

- **Kryterium Decyzyjne:** Jeśli wyliczona $p\text{-value} < 0.05$, hipoteza zerowa $H_0$ jest odrzucana na rzecz hipotezy alternatywnej $H_1$, co potwierdza statystyczną przewagę danego algorytmu AI.
