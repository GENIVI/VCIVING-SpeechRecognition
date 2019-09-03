import csv
import GeoLocationQuestionsProcess.consts.locationlog as consts_locationlog


def read_location_log(log_file_abs_path: str):
    csv_file = open(log_file_abs_path, "r")
    csv_reader = csv.reader(csv_file)

    locations = []
    row_index = 0
    column_indices = {}
    for row in csv_reader:
        if row_index == 0:
            column_indices = {
                consts_locationlog.COLUMN_TIMESTAMP: row.index(consts_locationlog.COLUMN_TIMESTAMP),
                consts_locationlog.COLUMN_LATITUDE: row.index(consts_locationlog.COLUMN_LATITUDE),
                consts_locationlog.COLUMN_LONGITUDE: row.index(consts_locationlog.COLUMN_LONGITUDE),
                consts_locationlog.COLUMN_ALTITUDE: row.index(consts_locationlog.COLUMN_ALTITUDE)
            }
        else:
            locations.append({
                consts_locationlog.COLUMN_TIMESTAMP: row[column_indices[consts_locationlog.COLUMN_TIMESTAMP]],
                consts_locationlog.COLUMN_LATITUDE: row[column_indices[consts_locationlog.COLUMN_LATITUDE]],
                consts_locationlog.COLUMN_LONGITUDE: row[column_indices[consts_locationlog.COLUMN_LONGITUDE]],
                consts_locationlog.COLUMN_ALTITUDE: row[column_indices[consts_locationlog.COLUMN_ALTITUDE]]
            })

    return locations
