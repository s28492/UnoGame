from datetime import datetime
import os
import pandas as pd


def merge_csv_files_in_chunks(output_filename='uno_game.csv', chunk_size=100_000):
    script_directory = os.path.abspath(os.path.dirname(__file__))
    print(script_directory)
    if not os.path.exists(script_directory+'/MergedCSV'):
        print("AAA")
        os.makedirs(script_directory+'/MergedCSV')
    output_filename = script_directory + f"/MergedCSV/{datetime.now().strftime('%Y%m%d_%H%M')}_"+output_filename
    for filename in os.listdir(script_directory):
        if filename.endswith('uno_game.csv'):
            print(filename)
            for chunk in pd.read_csv(script_directory+"/"+filename, chunksize=chunk_size):
                if not os.path.exists(output_filename):
                    chunk.to_csv(output_filename, mode='w', index=False, header=True)
                else:
                    chunk.to_csv(output_filename, mode='a', index=False, header=False)
    print(f'Wszystkie pliki CSV zostały połączone i zapisane do {output_filename}')


def operate_data():
    df = pd.read_csv('/mnt/587A903A7A90173A/Projekty/Python/UnoGame/Uno/games_data/MergedCSV/20240807_2148_uno_game.csv')
    df = df.loc[df["did_win"] == True]
    del df["round"]
    del df["direction"]
    del df["is_game_over"]
    del df["index_of_a_player"]
    del df["did_win"]
    del df["game_id"]
    df.reset_index(drop=True, inplace=True)
    print(df.columns)
    print(df.head())
    print(df.info())
    df.to_csv("Naive_Bayes_Data.csv", mode='a', index=False, header=True)


def read():
    merge_csv_files_in_chunks()

if __name__ == '__main__':
    read()
