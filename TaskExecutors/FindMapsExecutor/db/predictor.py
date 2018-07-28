import os, operator

from FindMapsExecutor.db.bigdata import BigDataFile
from FindMapsExecutor.db.locationdb import LocationDB
from FindMapsExecutor.db.preprocessors import LocationPreProcessor


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

    def get_real_location_for_phrase(self, phrase):
        real_locations_frequencies = self._get_real_locations_and_frequencies_for_assumed_location(phrase)
        real_location = max(real_locations_frequencies.items(), key=operator.itemgetter(1))[0]
        return real_location

    def get_geo_location_for_phrase(self, phrase, return_location_name=False):
        real_location = self.get_real_location_for_phrase(phrase)

        if real_location is not None:
            str_geo_location = self._mapper_db.get(real_location)
            if str_geo_location is not None:
                geo_location = str_geo_location.split(BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR)
                if return_location_name:
                    return real_location, geo_location[0], geo_location[1]
                else:
                    return geo_location[0], geo_location[1]
            else:
                if return_location_name:
                    return str_geo_location, None, None

        if return_location_name:
            return None, None, None
        else:
            return None, None

