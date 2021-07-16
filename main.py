from common.map_traj_to_grid import MapTrajToGrid
from common.mbr import MBR

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    # load data
    gy_taxi = pd.read_csv("./data/traj.csv", header=None).values
    # create mbr
    gy_mbr = MBR(26.548, 106.584, 26.704, 106.807)
    # create map_traj_to_map instance
    map_traj_to_map = MapTrajToGrid()

    arr = map_traj_to_map.map_traj_to_grid(gy_taxi, 0, 2, 3, gy_mbr, 64, if_wgs=False)
    # draw heatmap
    sns.set()
    sns.heatmap(arr, square=True)
    plt.show()
    print("ok")
