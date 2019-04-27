from common.mbr import MBR
from common.grid import Grid
from common.coord_transform import gcj02_to_wgs84

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class MapTrajToGrid:
    def __init__(self):
        self.traj = None
        self.time_idx = None
        self.lat_idx = None
        self.lng_idx = None

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
        print("++ coord gcj02 to wgs84 done")

    def map_traj_to_grid(self, traj, time_idx, lat_idx, lng_idx, mbr, grid_size, if_wgs=True):
        """
        map traj to grid
        :param traj: .npy格式的轨迹数据
        :param time_idx: traj中时间属性的索引
        :param lat_idx: traj中纬度属性的索引
        :param lng_idx: traj中经度属性的索引
        :param mbr: 轨迹的Bounding Box
        :param grid_size: 需划分的网格大小
        :param if_wgs: 轨迹坐标是否为wgs84坐标系
        :return:
        """
        self.traj = traj
        self.time_idx = time_idx
        self.lat_idx = lat_idx
        self.lng_idx = lng_idx
        # 若非wgs84坐标系,目前默认为gcj02,并转为wgs84
        if not if_wgs:
            self.transfer_coord_gcj02_to_wgs84()
        grid = Grid(mbr, grid_size, grid_size)
        res = np.zeros((grid_size, grid_size), dtype=np.int32)
        for i in range(len(self.traj)):
            lat = self.traj[i][self.lat_idx]
            lng = self.traj[i][self.lng_idx]
            try:
                row_idx, col_idx = grid.get_matrix_idx(lat, lng)
                res[row_idx, col_idx] += 1
            except IndexError:
                # print('({0}, {1}) is out of mbr, skip'.format(lat, lng))
                continue
        np.save("../data/map_traj_to_grid.npy", res)
        print("++ map traj to grid is done")
        return res


if __name__ == '__main__':
    # load data
    gy_taxi = pd.read_csv("../data/TaxiguiAU0676.csv", header=None).values
    # create mbr
    gy_mbr = MBR(26.548, 106.584, 26.704, 106.807)
    # create map_traj_to_map instance
    map_traj_to_map = MapTrajToGrid()
    arr = map_traj_to_map.map_traj_to_grid(gy_taxi, 0, 2, 3, gy_mbr, 128, if_wgs=False)
    # draw heatmap
    sns.set()
    sns.heatmap(arr, square=True)
    plt.show()
    print("ok")
