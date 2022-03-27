# Grid class for generating a dataframe that contains a coordinate grid
# pypi imports
import pandas as pd
import seaborn as sns

class grid:
    """
    This class takes the corner coordinates of a rectangle and returns a dataframe with all the coorindates 
    inbetween given level of decimal precision specified
    """

    def __init__(self, decimal_degrees=0, square_coords=(-5, 5, -10, 10)):
        """
        Initialize an instance of the grid class
        :inputs:
        - decimal_degress - int - decimal degrees of precision (n >= 0)
        - square_coords - list - list of float / int representing the bottom left and top right coordinates of a rectangle
        """
        self.square_coords = square_coords
        self.coords = self._build_coords(decimal_degrees, square_coords[0], square_coords[1], square_coords[2], square_coords[3])
        self.grid = self._build_grid(self.coords)
        sns.set(rc={'figure.facecolor':'cornflowerblue'})

    def _build_coords(self, decimal_degrees, min_lat, max_lat, min_long, max_long):
        """
        Builds a dictionary of coordinates to later be used to create a pandas.DataFrame
        :inputs:
        - decimal_degress - int - decimal degrees of precision (n >= 0)
        - min_lat - int - southwesterly most left latitude
        - max_lat - int - northeasterly most right latitude
        - min_long - int - southwesterly most longitude
        - max_long - int - northeasterly most longitude
        :output:
        - dict - dictionary of latitudes and longitudes
        """
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
        """ 
        Creates a pandas.DataFrame with coordinate pairs as the index
        :input:
        - coords - dict - output of the _build_coords function
        :output:
        pandas.DataFrame - df with lat, long, and a string index of the coordinate pairs
        """
        df = pd.DataFrame(coords)
        df["coord"] = df["lat"].astype(str) + ", " + df["long"].astype(str)
        df.set_index("coord", inplace=True)
        return df
        
    def show_coords(self):
        """
        Generate a scatterplot two show the points generated on the grid
        :inputs:
        - None.
        :output:
        - None.
        """
        sns.scatterplot(data=self.coords, x="long", y="lat")

if __name__ == "__main__":
    grid = grid(decimal_degrees=1, square_coords=(-5, 5, -10, 10))
    grid.show_coords()
