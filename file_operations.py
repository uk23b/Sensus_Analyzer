import os
import pandas as pd
from data_processing import detect_column_name_change


def save_columns_by_group(df, output_dir, original_filepath):
    # Extract the base name of the original file (without extension)
    original_file_base_name = os.path.splitext(os.path.basename(original_filepath))[0]

 # Ensure the output directory exists
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Directory created: {output_dir}")
        except Exception as e:
            print(f"Failed to create directory {output_dir}: {e}")
            return  # Exit the function if directory creation fails

    # Get the value of max_diff from detect_column_name_change
    max_diff = detect_column_name_change(df)[1]
    num_columns_per_county = max_diff

    # Get unique column details for file naming
    unique_column_details = get_unique_column_details(df)

    for group_index in range(num_columns_per_county):
        # Selecting every nth column starting from the current group index
        columns = [df.columns[i] for i in range(1 + group_index, len(df.columns), num_columns_per_county)]

        # Include the first descriptive column (like labels)
        group_df = df[['Label (Grouping)'] + columns]

        # Construct the filename using unique_column_details
        if group_index < len(unique_column_details):
            detail = unique_column_details[group_index].replace(' ', '_')
            filename = os.path.join(output_dir, f"{original_file_base_name}_{detail}.csv")
        else:
            filename = os.path.join(output_dir, f"{original_file_base_name}_{group_index}.csv")

        group_df.to_csv(filename, index=False)
        print(f"Saved {filename}")

def detect_column_name_change(df):
    """
    Detects the points at which the column name pattern changes in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame with column names to be checked.

    Returns:
    List[int]: A list of indices where the column name pattern changes.
    """
    change_indices = []
    previous_col_name = None

    for i, col in enumerate(df.columns):
        # Extract the main part of the column name (assumes format 'Name Detail')
        main_part = col.split()[0]

        if previous_col_name and main_part != previous_col_name:
            change_indices.append(i)
        
        previous_col_name = main_part
        
    max_diff_list = [change_indices[i + 1] - change_indices[i] for i in range(len(change_indices) - 1)]
    max_diff = max(max_diff_list, default=0)
    print('Max diff is', max_diff)

    return change_indices, max_diff

def get_unique_column_details(df):
    # Get the column names as a list
    column_names = df.columns.tolist()

    # Prepare a list to hold the processed column names
    output_file_column_names = []

    # Process each column name to extract the details after '!!'
    for item in column_names:
        # Split the column name by '!!' and take the last two parts
        column_update_temp = item.split('!!')[-2:]
        output_file_column_names.append(column_update_temp)

    # Get unique combinations of the last two parts
    unique_combinations = []
    for item in output_file_column_names:
        if item not in unique_combinations:
            unique_combinations.append(item)

    # Join the parts to create new column names
    unique_column_details = [' '.join(item) for item in unique_combinations]

    # Return the list excluding the first item (usually the descriptive label)
    return unique_column_details[1:]
