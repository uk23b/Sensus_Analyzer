import pandas as pd
from collections import Counter
import os, folium
import geopandas as gpd

def get_num_columns_per_county(df):
    """
    Determines the number of columns per county by examining the column headers.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame with column names to be checked.

    Returns:
    int: The number of columns per county.
    """
    county_set = set()
    for col in df.columns[1:]:  # Skip the first column which is 'Label (Grouping)'
        county_name = col.split("!!")[0]
        county_set.add(county_name)
    
    return (len(df.columns) - 1) // len(county_set)

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
        main_part = col.split()[0]

        if previous_col_name and main_part != previous_col_name:
            change_indices.append(i)
        
        previous_col_name = main_part
        
    max_diff_list = []
    for i in range(len(change_indices) - 1):
        max_diff_list.append(change_indices[i + 1] - change_indices[i])
    max_diff = max(max_diff_list)

    return change_indices, max_diff

def create_multi_state_map(state_codes):
    # Define the path to the data directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    # Paths to the state and county shapefiles
    state_shapefile = os.path.join(data_dir, 'cb_2022_us_state_500k', 'cb_2022_us_state_500k.shp')
    county_shapefile = os.path.join(data_dir, 'cb_2022_us_county_500k', 'cb_2022_us_county_500k.shp')

    # Read the state and county shapefiles
    states_df = gpd.read_file(state_shapefile)
    counties_df = gpd.read_file(county_shapefile)

    # Initialize Folium map at the US center
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Process each state code
    for state_code in state_codes:
        state_df = states_df[states_df['STUSPS'] == state_code.upper()]
        if state_df.empty:
            raise ValueError(f"Invalid state code or state not found: {state_code}")

        state_fips_code = state_df.iloc[0]['STATEFP']
        state_counties_df = counties_df[counties_df['STATEFP'] == state_fips_code]

        # Add state boundary to the map
        folium.GeoJson(state_df.to_json(), name=f'{state_code} State Boundary').add_to(m)

        # Add state counties to the map
        folium.GeoJson(state_counties_df.to_json(), name=f'{state_code} Counties').add_to(m)

    # Save the map to an HTML file
    filename = '_'.join(state_codes)  # Concatenates the state codes with underscores
    map_filename = os.path.join(script_dir, f'{filename}_counties.html')
    m.save(map_filename)
