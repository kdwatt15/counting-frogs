# Utilities used to support the frog counting challenge
# Standard imports
from math import radians, cos, sin, asin, sqrt

# Project imports
from .grid import grid

def build_grid(df, decimal_degrees):
    """
    Takes a dataframe with "lat" and "long" and initializes a grid object
    :inputs:
    - df - pandas.DataFrame - needs to have the columns "lat" and "long"
    - decimal_degrees - int -  with the number of decimal degrees of precision to be applied to the coordinates
    :output:
    - grid - (see ~\\utils\\grid.py for more details)
    """
    lat_min, lat_max = df["lat"].min(), df["lat"].max()
    long_min, long_max = df["long"].min(), df["long"].max()

    return grid(decimal_degrees=decimal_degrees, square_coords=(lat_min, lat_max, long_min, long_max))

def count_frogs(df, degrees, lat_col, long_col):
    """
    Takes a dataframe of frog observances and returns the number of observances at the specified decimal degree of precision
    :inputs:
    - df - pandas.DataFrame - frog observances
    - degrees - int - representing the decimal degrees of precision for coordinates
    - lat_col - str - name of the latitude column
    - long_col - str - name of the longitude column
    :output:
    - pandas.DataFrame - df with a lat, long, and frog_count based on the inputted frog observances
    """
    df["lat"] = round(df[lat_col],1)
    df["long"] = round(df[long_col],1)

    unique_coords = df[["lat", "long"]].copy()
    unique_coords = unique_coords.drop_duplicates()
    
    unique_coords["frog_count"] = 0

    for index, row in unique_coords.iterrows():
        a = df[
            (df["lat"] == row["lat"]) &
            (df["long"] == row["long"])
        ]
        unique_coords.at[index, "frog_count"] = len(a)

    unique_coords["coord"] = unique_coords["lat"].astype(str) + ", " + unique_coords["long"].astype(str)
    unique_coords.set_index("coord", inplace=True)

    empty_grid = build_grid(unique_coords, degrees)
    merged_grid = empty_grid.grid.merge(unique_coords, how="left")
    
    return merged_grid

def haversine_formula(coord1, coord2):
    """
    Source:

    Determine the distance between two coordinates accoring to the Haversine formula
    :inputs:
    - coord1 - list - first coordinates i.e. (lat, long)
    - coord2 - list - second coordinates i.e. (lat, long)
    :output:
    - int - distance in kim  
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

if __name__ == "__main__":
    pass
