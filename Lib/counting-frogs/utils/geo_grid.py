# Grid class for generating a dataframe that contains a coordinate grid
# pypi imports
import pandas as pd
import seaborn as sns
import multiprocessing.pool

class miniGrid:

    def __init__(self, decimal_degrees=0, square_coords=(-5, 5, -10, 10)):
        self.square_coords = square_coords

        if decimal_degrees == 0:
            increment = 1
        else:
            increment = 1 / (10 ** decimal_degrees)

        self.grid = self._build_grid(increment, square_coords[0], square_coords[1], square_coords[2], square_coords[3])
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

    def _build_grid(self, increment, min_lat, max_lat, min_long, max_long):
        grid = self._init_grid()
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

class grid(miniGrid):

    def __init__(self, decimal_degrees=1, square_coords=(-5, 5, -10, 10)):
        self.decimal_degrees = decimal_degrees
        self._sub_grid = self._split_grid(square_coords=square_coords)
        self.grid = pd.concat(self._create_grid(len(self._sub_grid), self._sub_grid))
        self.coords = self._write_coords(self.grid)

    def _create_mini_grid(self, square_coords):
        return miniGrid(decimal_degrees=self.decimal_degrees, square_coords=square_coords)

    def _split_grid(self, square_coords):
        # divide the grid into pieces to be processed asynchronously
        min_lat, max_lat = square_coords[0], square_coords[1]
        min_long, max_long = square_coords[2], square_coords[3]

        lat_range = abs(max_lat - min_lat)
        long_range = abs(max_long - min_long)

        corners = []

        x_inc = lat_range / min(100, lat_range)
        y_inc = long_range / min(100, long_range)

        lat = min_lat
        while lat < max_lat:
            long = min_long
            while long < max_long:
                corners.append((lat, lat+x_inc, long, long+y_inc))
                long+=y_inc
            lat+=x_inc

        return corners

    def _create_grid(self, processes, square_coords):
        pool = multiprocessing.pool.ThreadPool(processes=processes)
        return_list = pool.map(self._create_mini_grid, square_coords)
        pool.close()
        grid_list = [r.grid for r in return_list]
        return grid_list

if __name__ == "__main__":
    grid = grid(decimal_degrees=1, min_lat=-10, max_lat=0, min_long=-30, max_long=10)
    grid.show_grid()
