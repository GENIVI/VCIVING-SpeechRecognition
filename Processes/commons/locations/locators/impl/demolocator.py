from commons.locations.locators.abstracts import Locator
import csv
import commons.locations.log.consts.locationlog as consts_location_log


class DemoLocator(Locator):
    
    DATA_FILE_PATH = "D:/Dev/GENIVI/Projects/Processes/commons/locations/storage/20190911151603-60027-data.csv"
    LAST_INDEX_FILE_PATH = "D:/Dev/GENIVI/Projects/Processes/commons/locations/storage/20190911151603-60027-data.lastindex"

    def __init__(self):
        # Index 0 is the columns list, therefore never read according to the method get_location.
        self._last_read_index = 0
        with open(DemoLocator.LAST_INDEX_FILE_PATH, "a+") as last_index_file:
            last_index_file.seek(0)

            last_read_index_from_file = last_index_file.readline()
            if last_read_index_from_file != "":
                self._last_read_index = int(last_read_index_from_file)

        last_index_file.close()

        self._data_file = open(DemoLocator.DATA_FILE_PATH, "r")
        self._data_file_reader = csv.reader(self._data_file)

        self._data_file_rows_count = DemoLocator._get_file_location_count(DemoLocator.DATA_FILE_PATH)

    def __del__(self):
        self._data_file.close()

    @staticmethod
    def _get_file_location_count(file_path):
        return sum(1 for _ in open(file_path))

    def _update_last_index_file(self):
        with open(DemoLocator.LAST_INDEX_FILE_PATH, "w") as last_index_file:
            last_index_file.writelines([str(self._last_read_index)])

        last_index_file.close()

    def get_location(self):
        column_indices = {}

        for row_index, row in enumerate(self._data_file_reader):
            if row_index == 0:
                column_indices = {
                    consts_location_log.COLUMN_LATITUDE: row.index(consts_location_log.COLUMN_LATITUDE),
                    consts_location_log.COLUMN_LONGITUDE: row.index(consts_location_log.COLUMN_LONGITUDE)
                }
            elif row_index == self._last_read_index + 1:
                latitude = row[column_indices[consts_location_log.COLUMN_LATITUDE]]
                longitude = row[column_indices[consts_location_log.COLUMN_LONGITUDE]]
                altitude = 0

                self._data_file.seek(0)

                if row_index == self._data_file_rows_count - 1:
                    self._last_read_index = 0
                else:
                    self._last_read_index = row_index

                self._update_last_index_file()

                return str(latitude), str(longitude), str(altitude)
