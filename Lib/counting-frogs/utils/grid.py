# Grid class for generating a dataframe that contains a coordinate grid
# pypi imports
import pandas as pd
from numpy import average
import seaborn as sns
import multiprocessing.pool

class grid:

    def __init__(self, decimal_degrees=0, square_coords=(-5, 5, -10, 10)):
        self.square_coords = square_coords
        self.coords = self._build_coords(decimal_degrees, square_coords[0], square_coords[1], square_coords[2], square_coords[3])
        self.grid = self._build_grid(self.coords)
        sns.set(rc={'figure.facecolor':'cornflowerblue'})

    def _build_coords(self, decimal_degrees, min_lat, max_lat, min_long, max_long):
        if decimal_degrees == 0:
            increment = 1
        else:
            increment = 1 / (10 ** decimal_degrees)

        lat = min_lat

        lat_l, long_l = [], []

        while lat <= max_lat:
            long = min_long
            lat = round(lat, decimal_degrees)
            while long <= max_long:
                long = round(long, decimal_degrees)
                lat_l.append(lat)
                long_l.append(long),
                long += increment

            lat += increment

        coords = {"lat": lat_l, "long": long_l}

        return coords

    def _build_grid(self, coords):
        df = pd.DataFrame(coords)
        df["coord"] = df["lat"].astype(str) + ", " + df["long"].astype(str)
        df.set_index("coord", inplace=True)
        return df
        
    def show_coords(self):
        sns.scatterplot(data=self.coords, x="long", y="lat")

if __name__ == "__main__":
    grid = grid(decimal_degrees=1, square_coords=(-5, 5, -10, 10))
    grid.show_grid()
