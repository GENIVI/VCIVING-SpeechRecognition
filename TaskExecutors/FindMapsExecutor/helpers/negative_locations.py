import os
import json
from FindMapsExecutor.db.locationdb import GeoLocation
import FindMapsExecutor.consts.negative_locations as consts_negative_locations


class NegativeLocationDB:

    def __init__(self, db_file_path):
        self._db_file_path = db_file_path

        if not os.path.exists(db_file_path):
            db_file_creator_file = open(db_file_path, "a+")
            json.dump([], db_file_creator_file)
            db_file_creator_file.close()

        db_file = open(db_file_path, "r+")
        self._locations = json.load(db_file)
        db_file.close()

    def get_locations(self):
        return self._locations

    def add_location(self, geo_location: GeoLocation):
        self._locations.append({
            consts_negative_locations.DB_ENTRY_KEY_LOCATION_NAME: geo_location.get_location_name(),
            consts_negative_locations.DB_ENTRY_KEY_LATITUDE: geo_location.get_latitude(),
            consts_negative_locations.DB_ENTRY_KEY_LONGITUDE: geo_location.get_longitude(),
        })

        db_file = open(self._db_file_path, "r+")
        json.dump(self._locations, db_file)
        db_file.close()

    def location_exists(self, geo_location_to_search: GeoLocation):
        for geo_location in self.get_locations():
            if geo_location_to_search.get_location_name() == geo_location[consts_negative_locations.DB_ENTRY_KEY_LOCATION_NAME] or (geo_location_to_search.get_latitude() == geo_location[consts_negative_locations.DB_ENTRY_KEY_LATITUDE] and geo_location_to_search.get_longitude() == geo_location[consts_negative_locations.DB_ENTRY_KEY_LONGITUDE]):
                return True

        return False
