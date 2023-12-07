import pandas as pd
import geopandas as gpd

def calculate_statistics(row):
    # Parse and convert the row data to numeric values, handling percentages
    numeric_values = []
    for item in row:
        try:
            if item.endswith('%'):  # Check if the item is a percentage
                # Convert percentage to a decimal and append
                numeric_value = float(item.replace('%', '')) / 100
            else:
                # Handle non-percentage numbers (remove commas, etc.)
                numeric_value = float(item.replace(',', ''))
            numeric_values.append(numeric_value)
        except ValueError:
            # Skip non-numeric items
            continue

    # Convert the list to a pandas Series for statistical computation
    data_series = pd.Series(numeric_values)

    # Calculate statistics
    max_value = data_series.max()
    min_value = data_series.min()
    median_value = data_series.median()
    std_dev = data_series.std()
    mean_value = data_series.mean()

    return {
        "Max": max_value,
        "Min": min_value,
        "Median": median_value,
        "Standard Deviation": std_dev,
        "Mean": mean_value
    }
