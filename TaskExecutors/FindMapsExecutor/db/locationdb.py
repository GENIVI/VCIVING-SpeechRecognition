from bsddb3 import db


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
