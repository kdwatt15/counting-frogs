# general utitities
from .grid import grid

def build_grid(df, decimal_degrees):
    lat_min, lat_max = df["lat"].min(), df["lat"].max()
    long_min, long_max = df["long"].min(), df["long"].max()

    return grid(decimal_degrees=decimal_degrees, square_coords=(lat_min, lat_max, long_min, long_max))

def count_frogs(df, degrees, lat_col, long_col):
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

if __name__ == "__main__":
    pass
