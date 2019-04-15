from common.mbr import MBR


class Grid:
    """
    index order
    30 31 32 33 34...
    20 21 22 23 24...
    10 11 12 13 14...
    00 01 02 03 04...
    """
    def __init__(self, mbr, row_num, col_num):
        self.mbr = mbr
        self.row_num = row_num
        self.col_num = col_num
        self.lat_interval = (mbr.max_lat - mbr.min_lat) / float(row_num)
        self.lng_interval = (mbr.max_lng - mbr.min_lng) / float(col_num)

    def get_row_idx(self, lat):
        row_idx = int((lat - self.mbr.min_lat) // self.lat_interval)
        if row_idx >= self.row_num or row_idx < 0:
            raise IndexError("lat is out of mbr")
        return row_idx

    def get_col_idx(self, lng):
        col_idx = int((lng - self.mbr.min_lng) // self.lng_interval)
        if col_idx >= self.col_num or col_idx < 0:
            raise IndexError("lng is out of mbr")
        return col_idx

    def get_idx(self, lat, lng):
        return self.get_row_idx(lat), self.get_col_idx(lng)

    def get_matrix_idx(self, lat, lng):
        return self.row_num - 1 - self.get_row_idx(lat), self.get_col_idx(lng)

    def get_min_lng(self, col_idx):
        return self.mbr.min_lng + col_idx * self.lng_interval

    def get_max_lng(self, col_idx):
        return self.mbr.min_lng + (col_idx + 1) * self.lng_interval

    def get_min_lat(self, row_idx):
        return self.mbr.min_lat + row_idx * self.lat_interval

    def get_max_lat(self, row_idx):
        return self.mbr.min_lat + (row_idx + 1) * self.lat_interval

    def get_mbr_by_idx(self, row_idx, col_idx):
        min_lat = self.get_min_lat(row_idx)
        max_lat = self.get_max_lat(row_idx)
        min_lng = self.get_min_lng(col_idx)
        max_lng = self.get_max_lng(col_idx)
        return MBR(min_lat, min_lng, max_lat, max_lng)

    def get_mbr_by_matrix_idx(self, mat_row_idx, mat_col_idx):
        row_idx = self.row_num - 1 - mat_row_idx
        min_lat = self.get_min_lat(row_idx)
        max_lat = self.get_max_lat(row_idx)
        min_lng = self.get_min_lng(mat_col_idx)
        max_lng = self.get_max_lng(mat_col_idx)
        return MBR(min_lat, min_lng, max_lat, max_lng)
