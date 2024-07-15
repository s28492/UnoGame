from datetime import datetime
import os
import pandas as pd


def merge_csv_files_in_chunks(output_filename='merged.csv', chunk_size=100000):
    output_filename = f"MergedCSV/{datetime.now().strftime('%Y%m%d_%H%M')}_"+output_filename
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            # Odczytywanie pliku CSV w kawałkach
            for chunk in pd.read_csv(filename, chunksize=chunk_size):
                # Zapisywanie kawałka do pliku wynikowego
                # Jeżeli plik nie istnieje, tworzymy go z nagłówkiem
                if not os.path.exists(output_filename):
                    chunk.to_csv(output_filename, mode='w', index=False, header=True)
                else:
                    # Jeśli plik istnieje, dodajemy bez nagłówka
                    chunk.to_csv(output_filename, mode='a', index=False, header=False)

    print(f'Wszystkie pliki CSV zostały połączone i zapisane do {output_filename}')


# Wywołanie funkcji
merge_csv_files_in_chunks()
