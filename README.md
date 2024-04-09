#Uno Game

###Wprowadzenie
Niniejszy projekt opisuje implementację gry karcianej UNO w języku Python. Program obsługuje różne tryby rozgrywki, w tym:

- grę z ludźmi
- grę z botami
- obserwację rozgrywki pomiędzy botami

Gry są zarządzane przez wielowątkowość, co pozwala na równoczesną obsługę logiki gry i działań botów.

Składniki Gry:
Gra składa się z kilku kluczowych komponentów:

* Player: Reprezentuje gracza, zarówno ludzkiego, jak i bota oraz kontroluje poprawnośc decyzji gracza.
* Bot: Podklasa Player, implementująca logikę prostego bota z zaimplementowaną podstawową taktyką.
* Game: Zarządza stanem gry, w tym kartami, kolejnością graczy i zasadami.
* Card: Reprezentuje pojedynczą kartę w grze UNO, z atrybutami wartości i koloru oraz metodami pozwalającymi na interakcje między kartami.

## Jak grać
Aby rozpocząć rozgrywkę wystarczy uruchomić plik "main.py".

Gdy to zrobisz następnym krokiem jest wybranie trybu gry:

- Wybierz 1 jeśli chcesz grać z innymi ludźmi
- Wybierz 2 jeśli chcesz grać z botami
- Wybierz 3 jeśli chcesz obserwować grę botów
- Wybierz 4 jeśli twoim zamiarem jest gra zarówno z innymi ludźmi, jak i botami

W przypadku opcji 1 i 4, będziesz musiał podać nazwy wszystkich graczy. W przypadku opcji 2, 3, 4 będziesz musiał podać liczbę botów.

Po zainicjalizowaniu gry w terminalu pojawią się informacje typu:

- którego gracza tura
- ile kart ma w ręku
- jakie karty ma w ręku
- jakie efekty są na niego nałożone

Aby zagrać kartę należy podać jej wartość i kolor. Jeśli chcesz dobrać kartę musisz napisać "Draw", jeśli natomiast chcesz się poddać, napisz "Surrender"

##Talia
    19 czerwonych kart ponumerowanych od 0 do 9 (jedna karta z numerem 0 oraz po dwie karty z numerami od 1 do 9)
    19 zielonych kart ponumerowanych od 0 do 9 (jedna karta z numerem 0 oraz po dwie karty z numerami od 1 do 9)
    19 niebieskich kart ponumerowanych od 0 do 9 (jedna karta z numerem 0 oraz po dwie karty z numerami od 1 do 9)
    19 żółtych kart ponumerowanych od 0 do 9 (jedna karta z numerem 0 oraz po dwie karty z numerami od 1 do 9)

oraz kart funkcyjnych:

    8 kart stopu (Postój) po dwie z każdego koloru
    8 kart zmiany kierunku (Zmiana kierunku) po dwie z każdego koloru
    8 kart +2 (Weź dwie) po dwie z każdego koloru
    4 czarne karty +4 ze zmianą koloru (Wybierz kolor + Weź cztery)
    4 czarne karty zmiana koloru (Wybierz kolor)

## Zasady gry

Na początku gry rozdaje się po 7 kart każdemu graczowi i jedną z talii kładzie się na środek.  Gracz musi dopasować swoją kartę numerem, kolorem lub symbolem do odkrytej karty. Jeżeli gracz nie posiada żadnej karty pasującej do tej odkrytej, musi pociągnąć kartę z talii. Jeśli wyciągnięta karta pasuje do odkrytej, jeszcze w tej samej kolejce gracz może ją dołożyć. Jeżeli nie – ruch ma kolejny gracz. Nie ma przymusu w dokładaniu kart.

W talii są także karty specjalne takie jak Postój, Zmiana kierunku, Weź dwie, Wybierz kolor + Weź cztery, Wybierz kolor.

    Postój (jak 4 w makao) – następny gracz traci (stoi) kolejkę
    Zmiana kierunku (jak As w kunjo) – karta zmieniająca kierunek gry
    Weź dwie – następny gracz bierze dwie karty
    Wybierz kolor + Weź cztery – zagrywający kartę deklaruje zmianę koloru na dowolnie przez siebie wybrany, następny gracz bierze 4 karty.
    Wybierz kolor – zagrywający kartę deklaruje zmianę koloru na dowolnie przez siebie wybrany (jeden z kolorów dostępnych w grze)

Karty Postój, Zmiana kierunku, Weź dwie można kłaść do danego karcie koloru – natomiast karty Wybierz kolor + Weź cztery można kłaść na dowolną kartę.

# TODO: Dodać bota uczącego się gry za pomocą machine learningu