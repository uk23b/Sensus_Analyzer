import os
from gui_utils import setup_gui
from map_visualization import get_arkansas_counties_from_shapefile  # Import the new function

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    county_shapefile_path = os.path.join(script_dir, 'data', 'cb_2022_us_county_500k', 'cb_2022_us_county_500k.shp')

    # Retrieve the list of Arkansas counties from the shapefile
    arkansas_counties = get_arkansas_counties_from_shapefile(county_shapefile_path)

    # Initialize and run the GUI, passing the list of Arkansas counties
    setup_gui(county_shapefile_path, arkansas_counties)

if __name__ == '__main__':
    main()