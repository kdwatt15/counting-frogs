# Grid class for generating a dataframe that contains a coordinate grid
# pypi imports
import pandas as pd
import seaborn as sns

class Grid:

    def __init__(self, decimal_degrees=0, min_lat=-90, max_lat=90, min_long=-180, max_long=180):
        self.grid = self._build_grid(decimal_degrees, min_lat, max_lat, min_long, max_long)
        sns.set(rc={'figure.facecolor':'cornflowerblue'})
        self.coords = self._write_coords(self.grid)

    def _init_grid(self, data=None):
        columns = (
            "bottom_left_lat", 
            "bottom_left_long", 
            "bottom_right_lat", 
            "bottom_right_long", 
            "top_left_lat", 
            "top_left_long", 
            "top_right_lat", 
            "top_right_long"
        )
        
        return pd.DataFrame(data=data, columns=columns)

    def _build_grid(self, decimal_degrees, min_lat, max_lat, min_long, max_long):
        grid = self._init_grid()

        if decimal_degrees == 0:
            increment = 1
        else:
            increment = 1 / (10 ** decimal_degrees)
        
        lat = min_lat
    
        while lat < max_lat:
            long = min_long
            while long < max_long:
                square = self._init_grid(data=[[lat, long, lat, long+increment, lat+increment, long, lat+increment, long+increment]])
                grid = pd.concat((grid, square), ignore_index = True)
                long += increment
            lat += increment

        return grid

    def _write_coords(self, grid):
        bl = grid[["bottom_left_lat","bottom_left_long"]].copy()
        bl = bl.rename(columns={"bottom_left_lat": "lat", "bottom_left_long":"long"})
        br = grid[["bottom_right_lat", "bottom_right_long"]]
        br = br.rename(columns={"bottom_right_lat": "lat", "bottom_right_long":"long"})
        tl = grid[["top_left_lat","top_left_long"]].copy()
        tl = tl.rename(columns={"top_left_lat": "lat", "top_left_long":"long"})
        tr = grid[["top_right_lat", "top_right_long"]]
        tr = tr.rename(columns={"top_right_lat": "lat", "top_right_long":"long"})

        return pd.concat((bl, br, tl, tr))

    def show_grid(self):
        sns.scatterplot(data=self.coords, x="long", y="lat")


if __name__ == "__main__":
    grid = Grid(decimal_degrees=0, min_lat=-10, max_lat=0, min_long=-30, max_long=10)
    grid.show_grid()
