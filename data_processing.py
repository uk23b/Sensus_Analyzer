import pandas as pd

def get_county_names_from_csv(df):
    return list(set(col.split("!!")[0] for col in df.columns[1:]))

def get_num_columns_per_county(df):
    county_set = set(col.split("!!")[0] for col in df.columns[1:])
    return (len(df.columns) - 1) // len(county_set)

def detect_column_name_change(df):
    change_indices = [i for i, col in enumerate(df.columns) if col.split()[0] != df.columns[i - 1].split()[0]]
    max_diff = max(change_indices[i + 1] - change_indices[i] for i in range(len(change_indices) - 1))
    return change_indices, max_diff