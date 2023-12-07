
import pandas as pd
import json
import os

def load_output_data(output_dir):
    """
    Loads output data from the specified directory. Supports CSV and JSON files.
    
    Args:
    output_dir (str): The path to the output directory.
    
    Returns:
    dict: A dictionary with filenames as keys and loaded data as values.
    """
    loaded_data = {}
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if filename.endswith('.csv'):
            loaded_data[filename] = pd.read_csv(file_path)
        elif filename.endswith('.json'):
            with open(file_path, 'r') as file:
                loaded_data[filename] = json.load(file)
    
    return loaded_data
