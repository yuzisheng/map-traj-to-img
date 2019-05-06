class MBR:
    """
    minimum bounding rectangular
    """
    def __init__(self, min_lat, min_lng, max_lat, max_lng):
        self.min_lat = min_lat
        self.min_lng = min_lng
        self.max_lat = max_lat
        self.max_lng = max_lng

    def contains(self, lat, lng):
        """
        if mbr contains this point(lat, lng)
        :param lat:
        :param lng:
        :return:
        """
        return self.min_lat <= lat <= self.max_lat and self.min_lng <= lng <= self.max_lng

    def center(self):
        """
        :return: the center of mbr
        """
        return (self.min_lat + self.max_lat) / 2.0, (self.min_lng + self.max_lng) / 2.0
