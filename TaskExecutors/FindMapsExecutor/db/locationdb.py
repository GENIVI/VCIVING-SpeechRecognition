from bsddb3 import db
from FindMapsExecutor.db.bigdata import BigDataFile


class LocationDB:

    FLAG_DB_CREATE = db.DB_CREATE
    FLAG_DB_RDONLY = db.DB_RDONLY
    FLAG_DB_THREADED = db.DB_THREAD

    def __init__(self, file_path, db_flag):
        self._db = db.DB()
        self._db.open(file_path, None, db.DB_HASH, db_flag)

    @staticmethod
    def _encode_to_bytes(to_convert : str):
        return bytes(to_convert, encoding="utf8")

    @staticmethod
    def _decode_from_bytes(to_convert : bytes):
        return to_convert.decode("utf-8")

    def insert(self, key : str, value : str):
        self._db.put(self._encode_to_bytes(key), value)

    def get(self, key):
        bytes_value = self._db.get(self._encode_to_bytes(key))
        if bytes_value is not None:
            bytes_value = self._decode_from_bytes(bytes_value)

        return bytes_value

    def close(self):
        self._db.close()


class GeoLocation:

    ARG_LOCATION_NAME = "location_name"
    ARG_LATITUDE = "latitude"
    ARG_LONGITUDE = "longitude"

    ARG_PARSE_STRING_GEOLOCATION = "parse_string_geolocation"

    def __init__(self, **kwargs):
        if GeoLocation.ARG_LOCATION_NAME in kwargs:
            if GeoLocation.ARG_LATITUDE in kwargs and GeoLocation.ARG_LONGITUDE in kwargs:
                self._location_name = kwargs[GeoLocation.ARG_LOCATION_NAME]
                self._latitude = kwargs[GeoLocation.ARG_LATITUDE]
                self._longitude = kwargs[GeoLocation.ARG_LONGITUDE]
            elif GeoLocation.ARG_PARSE_STRING_GEOLOCATION in kwargs:
                location_data = kwargs[GeoLocation.ARG_PARSE_STRING_GEOLOCATION].split(BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR)
                self._location_name = kwargs[GeoLocation.ARG_LOCATION_NAME]
                self._latitude = location_data[0]
                self._longitude = location_data[1]
            else:
                self._location_name = kwargs[GeoLocation.ARG_LOCATION_NAME]
                self._latitude = None
                self._longitude = None
        else:
            self._location_name = None
            self._latitude = None
            self._longitude = None

    def get_location_name(self):
        return self._location_name

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude
