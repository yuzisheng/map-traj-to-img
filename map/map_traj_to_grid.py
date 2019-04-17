from common.mbr import MBR
from common.grid import Grid
from common.coord_transform import gcj02_to_wgs84

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class MapTrajToGrid:
    def __init__(self, traj, time_idx, lat_idx, lng_idx):
        self.traj = traj
        self.time_idx = time_idx
        self.lat_idx = lat_idx
        self.lng_idx = lng_idx

    def transfer_coord_gcj02_to_wgs84(self):
        """
        transfer coord from gcj02 to wgs84
        :return:
        """
        for i in range(len(self.traj)):
            lnglat_wgs = gcj02_to_wgs84(self.traj[i][self.lng_idx], self.traj[i][self.lat_idx])
            self.traj[i][self.lng_idx] = lnglat_wgs[0]
            self.traj[i][self.lat_idx] = lnglat_wgs[1]
        pd.DataFrame(data=self.traj, columns=None).to_csv("../data/traj_wgs.csv", index=False)
        print("coord gcj02 to wgs84 done")

    def map_traj_to_grid(self, min_lat, min_lng, max_lat, max_lng, grid_size):
        """
        map traj to grid
        :param min_lat:
        :param min_lng:
        :param max_lat:
        :param max_lng:
        :param grid_size:
        :return:
        """
        mbr = MBR(min_lat, min_lng, max_lat, max_lng)
        grid = Grid(mbr, grid_size, grid_size)
        res = np.zeros((grid_size, grid_size), dtype=np.int32)
        for i in range(len(self.traj)):
            lat = self.traj[i][self.lat_idx]
            lng = self.traj[i][self.lng_idx]
            try:
                row_idx, col_idx = grid.get_matrix_idx(lat, lng)
                res[row_idx, col_idx] += 1
            except IndexError:
                print('({0}, {1}) is out of mbr, skip'.format(lat, lng))
                continue
        np.save("../data/map_traj_to_grid.npy", res)
        print("map traj to grid is done")
        return res


if __name__ == '__main__':
    # load data
    data = pd.read_csv("../data/TaxiguiAU0676.csv", header=None).values
    map_traj_to_map = MapTrajToGrid(data, time_idx=0, lat_idx=2, lng_idx=3)
    map_traj_to_map.transfer_coord_gcj02_to_wgs84()
    arr = map_traj_to_map.map_traj_to_grid(min_lat=26.337, min_lng=106.389,
                                           max_lat=26.788, max_lng=106.966, grid_size=128)
    # draw heatmap
    sns.set()
    sns.heatmap(arr, square=True)
    plt.show()
    print("ok")
