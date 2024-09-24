import os
from gui_utils import setup_gui
from map_visualization import get_arkansas_counties_from_shapefile  

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    county_shapefile_path = os.path.join(script_dir, 'data', 'cb_2022_us_county_500k', 'cb_2022_us_county_500k.shp')

    arkansas_counties = get_arkansas_counties_from_shapefile(county_shapefile_path)

    setup_gui(county_shapefile_path, arkansas_counties)

if __name__ == '__main__':
    main()
