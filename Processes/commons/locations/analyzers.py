import commons.locations.log.utils.rw as utils_location_log
import commons.locations.log.consts.locationlog as consts_location_log
from haversine import haversine, Unit
import math
import numpy as np
from math import degrees, sin, asin, sqrt
import commons.locations.config.analyzers as config_analyzers
import commons.locations.consts.analyzers as consts_analyzers
import scipy.cluster.hierarchy as hcluster


class GeoLocationLogAnalyzer:

    def __init__(self, log_file_path: str, location_update_interval: int):
        self._log_file_path = log_file_path
        self._location_data = utils_location_log.read_location_log(log_file_path)

        # Whenever the default location update interval was used, the default stop determination threshold was used to
        # determine stop locations.
        self._stop_determination_threshold_location_count = (consts_location_log.DEFAULT_STOP_DETERMINATION_THRESHOLD / consts_location_log.DEFAULT_UPDATE_INTERVAL) * location_update_interval

    def refresh_data(self):
        self._location_data = utils_location_log.read_location_log(self._log_file_path)

    def get_locations_count(self):
        return len(self._location_data)

    def get_consecutive_distances(self):
        distances = []
        for location_index in range(len(self._location_data) - 1):
            location_1 = self._location_data[location_index]
            location_1_latitude = location_1[consts_location_log.COLUMN_LATITUDE]
            location_1_longitude = location_1[consts_location_log.COLUMN_LONGITUDE]
            location_1_altitude = location_1[consts_location_log.COLUMN_ALTITUDE]
            location_1_sph_crds = (location_1_latitude, location_1_longitude)

            location_2 = self._location_data[location_index + 1]
            location_2_latitude = location_2[consts_location_log.COLUMN_LATITUDE]
            location_2_longitude = location_2[consts_location_log.COLUMN_LONGITUDE]
            location_2_altitude = location_2[consts_location_log.COLUMN_ALTITUDE]
            location_2_sph_crds = (location_2_latitude, location_2_longitude)

            # Retain SI Units
            haversine_distance = haversine(location_2_sph_crds, location_1_sph_crds, Unit.METERS)
            altitude_difference = location_2_altitude - location_1_altitude
            real_distance = math.sqrt((haversine_distance**2) + (altitude_difference**2))

            distances.append(real_distance)

        return distances

    def get_consecutive_time_gaps(self):
        time_gaps = []
        for location_index in range(len(self._location_data) - 1):
            location_1 = self._location_data[location_index]
            location_1_timestamp = location_1[consts_location_log.COLUMN_TIMESTAMP]

            location_2 = self._location_data[location_index + 1]
            location_2_timestamp = location_2[consts_location_log.COLUMN_TIMESTAMP]

            # Retain SI Units
            time_gap = location_2_timestamp - location_1_timestamp
            time_gaps.append(time_gap)

        return time_gaps

    def get_instantaneous_velocities(self):
        distances = self.get_consecutive_distances()
        time_gaps = self.get_consecutive_time_gaps()

        velocities = []
        for motion_index in range(len(distances)):
            distance = distances[motion_index]
            time_gap = time_gaps[motion_index]

            velocity = distance / time_gap
            velocities.append(velocity)

        return velocities

    def get_location_clusters(self):
        latitudes, longitudes = [], []
        for location in self._location_data:
            latitudes.append(location[consts_location_log.COLUMN_LATITUDE])
            longitudes.append(location[consts_location_log.COLUMN_LONGITUDE])

        np_locations = np.array([latitudes, longitudes]).T
        segment_cutoff_threshold_in_degrees = degrees(asin(sqrt(2) * sin((config_analyzers.SEGMENT_CUTOFF_THRESHOLD * consts_analyzers.KMS_IN_METER) / (2 * consts_analyzers.AVERAGE_EARTH_RADIUS))))
        np_locations_clusters = hcluster.fclusterdata(np_locations, segment_cutoff_threshold_in_degrees, criterion="distance")

        location_data_with_clusters = []
        for location_index, cluster in np.ndenumerate(np_locations_clusters):
            location_data = self._location_data[location_index[0]]
            location_data[consts_location_log.COLUMN_CLUSTER] = cluster
            location_data_with_clusters.append(location_data)

        return location_data_with_clusters

    def get_clusters(self, location_clusters: list=None):
        if location_clusters is not None:
            location_data_with_clusters = location_clusters
        else:
            location_data_with_clusters = self.get_location_clusters()

        return list(set([location[consts_location_log.COLUMN_CLUSTER] for location in location_data_with_clusters]))

    def get_cluster_heat_map(self, location_clusters: list=None):
        if location_clusters is not None:
            location_data_with_clusters = location_clusters
        else:
            location_data_with_clusters = self.get_location_clusters()

        unique_clusters = self.get_clusters(location_clusters)

        cluster_heat_map = [0 for _ in range(len(unique_clusters) + 1)]
        for location in location_data_with_clusters:
            location_cluster = location[consts_location_log.COLUMN_CLUSTER]
            cluster_heat_map[location_cluster] += 1

        return cluster_heat_map

    def get_stop_clusters(self, location_clusters: list=None):
        cluster_heat_map = self.get_cluster_heat_map(location_clusters)

        stop_clusters = []
        for cluster, location_points_count in enumerate(cluster_heat_map):
            if location_points_count > self._stop_determination_threshold_location_count:
                stop_clusters.append(cluster)

        return stop_clusters

    def is_a_stop_cluster(self, cluster: int, location_clusters: list=None):
        return cluster in self.get_stop_clusters(location_clusters)
