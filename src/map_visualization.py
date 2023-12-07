
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def plot_county_data(csv_file_path, shapefile_path, column_to_plot):
    # Load the CSV data
    df = pd.read_csv(csv_file_path)
    
    # Load the shapefile containing county geometries
    gdf = gpd.read_file(shapefile_path)

    # Make sure the data and the shapefile match on the county names
    gdf['NAME'] = gdf['NAME'].apply(lambda x: x + ' County, Arkansas')

    # Merge the CSV data with the shapefile dataframe on the county names
    merged_gdf = gdf.merge(df, left_on='NAME', right_on='Label (Grouping)', how='left')

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged_gdf.plot(column=column_to_plot, ax=ax, legend=True,
                    legend_kwds={'label': "Value by County",
                                 'orientation': "horizontal"})
    plt.show()

# Example usage:
# csv_file_path = 'path_to_your_csv_file'  # Replace with the path to your CSV file
# shapefile_path = 'path_to_your_shapefile'  # Replace with the path to the Arkansas shapefile
# column_to_plot = 'YourColumnName'  # Replace with the column you want to plot

# plot_county_data(csv_file_path, shapefile_path, column_to_plot)

def plot_county_row_data(row_data, shapefile_path):
    # The function assumes 'row_data' is a pandas Series with county data
    # 'shapefile_path' is the path to the shapefile containing county geometries
    
    # Load the shapefile containing county geometries
    gdf = gpd.read_file(shapefile_path)

    # The row data keys are county names with additional descriptions; clean them to match the shapefile
    county_data = row_data.iloc[0]  # Extract the data from the series
    county_data.index = county_data.index.str.split('!!').str[0]  # Keep only the county names
    
    # Merge the row data with the shapefile dataframe on the county names
    gdf['NAME'] = gdf['NAME'] + ' County, Arkansas'  # Adjust the names to match the row data keys
    gdf = gdf.set_index('NAME').join(county_data)
    
    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column=gdf.columns[-1], ax=ax, legend=True,  # Plot the last column, which is the row data
             legend_kwds={'label': "Value by County", 'orientation': "horizontal"})
    plt.show()
