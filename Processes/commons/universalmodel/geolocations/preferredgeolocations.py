import commons.universalmodel.geolocations.config.files as config_file_paths
import os
import json
import commons.universalmodel.geolocations.consts.keys as consts_keys


class PreferredGeoLocation:

    def __init__(self, location_code: str, latitude: float, longitude: float):
        self._location_code = location_code
        self._latitude = latitude
        self._longitude = longitude

    def get_location_code(self):
        return self._location_code

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude


class PreferredGeoLocationsModel:

    def __init__(self, processes_abs_folder_path: str):
        self._model_file_path = processes_abs_folder_path + "/" + config_file_paths.PREFERRED_GEO_LOCATIONS_MODEL_FILE_PATH

        if not os.path.exists(self._model_file_path):
            model_file_creator_file = open(self._model_file_path, "a+")
            json.dump([], model_file_creator_file)
            model_file_creator_file.close()

        model_file = open(self._model_file_path, "r+")
        self._preferred_locations = json.load(model_file)
        model_file.close()

    def get_all_locations(self):
        return self._preferred_locations

    def add_location(self, preferred_geo_location: PreferredGeoLocation):
        self._preferred_locations.append({
            consts_keys.PreferredGeoLocationModelKeys.LOCATION_CODE: preferred_geo_location.get_location_code(),
            consts_keys.PreferredGeoLocationModelKeys.LATITUDE: preferred_geo_location.get_latitude(),
            consts_keys.PreferredGeoLocationModelKeys.LONGITUDE: preferred_geo_location.get_longitude(),
        })

        model_file = open(self._model_file_path, "r+")
        json.dump(self._preferred_locations, model_file)
        model_file.close()
