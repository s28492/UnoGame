# Dockerfile - Wersja Ostateczna

# 1. Obraz bazowy
FROM python:3.11-slim

# 2. Ustawiamy główny folder roboczy
WORKDIR /app

# 3. Kopiujemy TYLKO plik z zależnościami
COPY requirements.txt .
# 4. Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiujemy CAŁY projekt (z folderem Uno) do /app
COPY . .

# 6. Określamy domyślną komendę (nie jest kluczowa, ale to dobra praktyka)
CMD [ "bash" ]