import os, operator

from FindMapsExecutor.db.bigdata import BigDataFile
from FindMapsExecutor.db.locationdb import LocationDB
from FindMapsExecutor.db.preprocessors import LocationPreProcessor
from FindMapsExecutor.db.locationdb import GeoLocation


class Predictor:

    def __init__(self, db_file_path, mapper_file_path):
        if not os.path.exists(os.path.abspath(db_file_path)) or not os.path.exists(os.path.abspath(mapper_file_path)):
            self._init_success = False
        else:
            self._location_db = LocationDB(db_file_path, LocationDB.FLAG_DB_RDONLY)
            self._mapper_db = LocationDB(mapper_file_path, LocationDB.FLAG_DB_RDONLY)

    # Searches the database for the separate chunks of the assumed location.
    # Returns a dictionary of real location names which maps to their frequencies of existence.
    def _get_real_locations_and_frequencies_for_assumed_location(self, assumed_location):
        pre_proc = LocationPreProcessor([assumed_location])
        pre_proc.pre_process()
        assumed_location = pre_proc.get_locations()[0]

        real_locations = {}
        for i in range(len(assumed_location)):
            # for j in range(i + 1, len(assumed_location)):
            chunk_assumed_location = assumed_location[i:len(assumed_location)]
            str_real_locations_for_chunk = self._location_db.get(chunk_assumed_location)

            if str_real_locations_for_chunk is not None:
                real_locations_for_chunk = str_real_locations_for_chunk.split(BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR)
                for real_location_for_chunk in real_locations_for_chunk:
                    if real_location_for_chunk not in real_locations:
                        real_locations[real_location_for_chunk] = 1
                    else:
                        real_locations[real_location_for_chunk] += 1 * len(chunk_assumed_location)

        return real_locations

    def _get_real_locations_and_norm_frequencies_for_assumed_location(self, phrase):
        real_location_frequencies = self._get_real_locations_and_frequencies_for_assumed_location(phrase)
        factor = 1.0 / max(real_location_frequencies.items(), key=operator.itemgetter(1))[1]
        for real_location in real_location_frequencies:
            real_location_frequencies[real_location] *= factor

        return real_location_frequencies

    def get_geo_locations_from_real_locations_and_frequencies(self, real_location_frequencies):
        geo_location_frequencies = {}
        for real_location in real_location_frequencies:
            str_geo_location = self._mapper_db.get(real_location)
            if str_geo_location is not None:
                kwargs = {
                    GeoLocation.ARG_LOCATION_NAME: real_location,
                    GeoLocation.ARG_PARSE_STRING_GEOLOCATION: str_geo_location
                }
            else:
                kwargs = {
                    GeoLocation.ARG_LOCATION_NAME: real_location,
                    GeoLocation.ARG_LATITUDE: None,
                    GeoLocation.ARG_LONGITUDE: None
                }
            geo_location = GeoLocation(**kwargs)
            geo_location_frequencies[geo_location] = real_location_frequencies[real_location]

        return geo_location_frequencies

    def get_geo_locations_and_frequencies_for_phrase(self, phrase):
        real_location_frequencies = self._get_real_locations_and_frequencies_for_assumed_location(phrase)
        return self.get_geo_locations_from_real_locations_and_frequencies(real_location_frequencies)

    def get_geo_locations_and_norm_frequencies_for_phrase(self, phrase):
        real_location_norm_frequencies = self._get_real_locations_and_norm_frequencies_for_assumed_location(phrase)
        return self.get_geo_locations_from_real_locations_and_frequencies(real_location_norm_frequencies)

    def get_real_location_for_phrase(self, phrase):
        real_locations_frequencies = self._get_real_locations_and_frequencies_for_assumed_location(phrase)
        real_location = max(real_locations_frequencies.items(), key=operator.itemgetter(1))[0]
        return real_location

    def get_geo_location_for_phrase(self, phrase):
        real_location = self.get_real_location_for_phrase(phrase)

        if real_location is not None:
            str_geo_location = self._mapper_db.get(real_location)
            if str_geo_location is not None:
                kwargs = {
                    GeoLocation.ARG_LOCATION_NAME: real_location,
                    GeoLocation.ARG_PARSE_STRING_GEOLOCATION: str_geo_location
                }
                return GeoLocation(**kwargs)
            else:
                kwargs = {
                    GeoLocation.ARG_LOCATION_NAME: real_location,
                    GeoLocation.ARG_LATITUDE: None,
                    GeoLocation.ARG_LONGITUDE: None
                }
                return GeoLocation(**kwargs)

        return None

