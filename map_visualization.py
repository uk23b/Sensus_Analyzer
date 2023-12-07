import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from data_processing import get_county_names_from_csv
from tkinter import filedialog
import mpl_toolkits.basemap as Basemap
import tkinter as tk
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL
import io, os


def get_arkansas_counties_from_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    arkansas_gdf = gdf[gdf['STUSPS'] == 'AR']
    arkansas_counties = arkansas_gdf['NAME'].tolist()
    return arkansas_counties

def get_county_list_from_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    counties = gdf['NAME'].tolist()
    return counties

# Define a function to convert a Matplotlib figure to a PhotoImage
def plt_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    return ImageTk.PhotoImage(img)


def extract_label_from_filename(filename):
    # Assuming the filename is structured like 'poverty_Total_Estimate.csv'
    
    # return the name of interest (e.g. 'poverty Total Estimate') instead of full path name
    label = os.path.splitext(os.path.basename(filename))[0].replace('_', ' ')
    return label


def plot_county_data(cleaned_data, shapefile_path, title):
    arkansas_gdf = gpd.read_file(shapefile_path)
    arkansas_gdf = arkansas_gdf[arkansas_gdf['STUSPS'] == 'AR']
    arkansas_gdf = arkansas_gdf.merge(cleaned_data, left_on='NAME', right_index=True, how='left')
    arkansas_gdf['Population'] = pd.to_numeric(arkansas_gdf['Population'].str.replace(',', ''), errors='coerce')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    arkansas_gdf.plot(column='Population', ax=ax, legend=True, legend_kwds={'orientation': "horizontal"})
    plt.title(title)
    plt.show()

def plot_county_row_data(row_data, shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    cleaned_county_names = row_data.index.str.split('!!').str[0]
    county_data = pd.DataFrame(row_data.values, index=cleaned_county_names, columns=['Population'])
    merged_gdf = gdf.set_index('NAME').join(county_data, how='left')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged_gdf.plot(column='Population', ax=ax, legend=True, legend_kwds={'label': "Value by County", 'orientation': "horizontal"})
    plt.show()
    

def get_state_boundaries(shapefile_path):
    # Read the shapefile to get state boundaries
    gdf = gpd.read_file(shapefile_path)
    state_boundaries = {}

    # Group data by state abbreviation (STUSPS) and calculate the boundaries
    for state_abbr, state_data in gdf.groupby('STUSPS'):
        llcrnrlon = state_data.bounds.minx.min()
        llcrnrlat = state_data.bounds.miny.min()
        urcrnrlon = state_data.bounds.maxx.max()
        urcrnrlat = state_data.bounds.maxy.max()
        state_boundaries[state_abbr] = (llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat)

    return state_boundaries

def plot_selected_row(df, selected_row_name, county_shapefile_path, filename, selected_counties=None):
    if selected_row_name not in df['Label (Grouping)'].values:
        print(f"Selected row '{selected_row_name}' does not exist in the DataFrame.")
        return

    # Filter the DataFrame to get the selected row's data
    selected_row = df[df.iloc[:, 0] == selected_row_name]
    selected_row_data = selected_row.iloc[0, 1:]

    # Clean up the column names
    selected_row_data.index = (
        selected_row_data.index.str.split('!!').str[0]
        .str.replace(' County', '')
        .str.split(',').str[0]
    )

    # Remove non-numeric characters, including '±', and convert to float or integer
    selected_row_data = (
        selected_row_data.str.replace('[^0-9.-]', '', regex=True)  # Remove non-numeric characters
        .str.rstrip('%')  # Remove percentage symbol
        .replace('', '0')  # Replace empty strings with '0'
        .astype(float)
        .fillna(float('nan'))  # Fill NaN values with NaN
    )

    # Read the shapefile and filter for Arkansas
    gdf = gpd.read_file(county_shapefile_path)
    gdf = gdf[gdf['STUSPS'] == 'AR']

    # Create a DataFrame for county data
    county_data = pd.DataFrame(selected_row_data.values, index=selected_row_data.index, columns=['Population'])

    # Create a dictionary from county_data
    county_data_dict = county_data.to_dict()['Population']

    # Create a mapping between shapefile county names and population values
    mapping = {county: county_data_dict.get(county, float('nan')) for county in gdf['NAME']}

    # Get min and max values for color scaling
    non_nan_values = [value for value in mapping.values() if not pd.isna(value)]
    vmin, vmax = min(non_nan_values, default=0), max(non_nan_values, default=0)

    # Plot the data on a map with the RdBu colormap
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))
    gdf['Population'] = gdf['NAME'].map(mapping)

    # Create a colormap
    cmap = plt.cm.RdBu
    norm = plt.Normalize(vmin=vmin, vmax=vmax)

    # Plot all counties with color based on the mapping
    gdf['Population'].fillna(float('nan'), inplace=True)  # Fill NaN values for counties with no data

    # Plot selected counties with a different color if specified
    if selected_counties:
        selected_counties_set = set(selected_counties)
        cmap = plt.cm.RdBu  # Use RdBu colormap for selected counties

    # Plot the data and assign it to a variable
    plot = gdf.plot(column='Population', cmap=cmap, legend=False, vmin=vmin, vmax=vmax, ax=ax)

    # Extract label from filename
    plot_label = extract_label_from_filename(filename)

    # Add a colorbar with a label - Now explicitly linked to the plot
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label(plot_label)  # Set the label for the colorbar

    # Set aspect ratio to be equal for a tighter fit
    ax.set_aspect('equal')

    # Automatically adjust the extent to fit the map
    ax.autoscale()

    

    # Add annotations (values and county names) to the map for selected counties
    for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['Population']):
        if not pd.isna(label):  # Only add annotations for non-NaN (valid) values
            county_name = gdf[gdf.geometry.centroid.x == x]['NAME'].values[0]
            label_text = "N/A" if pd.isna(label) else f"{int(label)}"
            ax.text(x, y, label_text, fontsize=8, ha='center', va='center', color='black')
            ax.text(x, y - 0.05, county_name, fontsize=5, ha='center', va='center', color='black')

    plt.title(f"Population Data for {selected_row_name}")
    ax.set_axis_off()







    
    plt.show()