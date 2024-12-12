import pandas as pd
import numpy as np
pd.set_option('future.no_silent_downcasting', True)

def prepare_data_for_learning(df: pd.DataFrame):
    if "did_win" in df.columns:
        df = df.loc[df["did_win"]]
        del df["did_win"]
    df.drop(df.loc[df["card_played"] == "Stop Stop"].index,inplace=True)
    if "game_id" in df.columns:
        del df["game_id"]
    df.reset_index(drop=True, inplace=True)
    return df

def decode_data(df: pd.DataFrame, label_encoders):
    new_df = pd.DataFrame()
    for column in df.columns.to_list():
        new_df[column] = df[column].replace(label_encoders[column].keys(), label_encoders[column].values())

    return new_df


def encode_data_with_label(df: pd.DataFrame, label_encoders):
    for column in df.columns.to_list():
        df[column] = df[column].replace(label_encoders[column].values(), label_encoders[column].keys()).astype(np.int32)
    return df

def encode_data(df: pd.DataFrame):
    label_encoders = {}
    for column in df.columns.to_list():
        df[column], label_encoders[column] = create_column_label(df[column])
    return df, label_encoders


def create_column_label(column: pd.Series):
    counted_values = column.value_counts()
    encoded_column = {}
    for i in range(counted_values.shape[0]):
        encoded_column[i] = counted_values.index.to_list()[i]
    distinct_values = column.nunique()
    if column.dtype == "bool":
        column = column.astype(bool)
    else:
        if distinct_values < 256:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint8)
        elif distinct_values < 65536:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint16)
        elif distinct_values < 4294967295:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint32)
        elif distinct_values < 4294967296:
            column = column.replace(encoded_column.values(), encoded_column.keys()).astype(np.uint64)
    return column, encoded_column
