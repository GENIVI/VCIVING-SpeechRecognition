import csv
import os
from commons.locations.log.consts import locationlog as consts_location_log


def _create_log_file_if_not_exists(log_file_abs_path: str):
    log_file_exists = os.path.isfile(log_file_abs_path)

    if not log_file_exists:
        with open(log_file_abs_path, "a+", newline="") as log_file:
            log_file_writer = csv.writer(log_file)
            if not log_file_exists:
                log_file_writer.writerow([consts_location_log.COLUMN_TIMESTAMP, consts_location_log.COLUMN_LATITUDE, consts_location_log.COLUMN_LONGITUDE, consts_location_log.COLUMN_ALTITUDE])

        log_file.close()


def read_location_log(log_file_abs_path: str):
    _create_log_file_if_not_exists(log_file_abs_path)

    csv_file = open(log_file_abs_path, "r")
    csv_reader = csv.reader(csv_file)

    locations = []
    row_index = 0
    column_indices = {}
    for row in csv_reader:
        if row_index == 0:
            column_indices = {
                consts_location_log.COLUMN_TIMESTAMP: row.index(consts_location_log.COLUMN_TIMESTAMP),
                consts_location_log.COLUMN_LATITUDE: row.index(consts_location_log.COLUMN_LATITUDE),
                consts_location_log.COLUMN_LONGITUDE: row.index(consts_location_log.COLUMN_LONGITUDE),
                consts_location_log.COLUMN_ALTITUDE: row.index(consts_location_log.COLUMN_ALTITUDE)
            }
        else:
            locations.append({
                consts_location_log.COLUMN_TIMESTAMP: row[column_indices[consts_location_log.COLUMN_TIMESTAMP]],
                consts_location_log.COLUMN_LATITUDE: row[column_indices[consts_location_log.COLUMN_LATITUDE]],
                consts_location_log.COLUMN_LONGITUDE: row[column_indices[consts_location_log.COLUMN_LONGITUDE]],
                consts_location_log.COLUMN_ALTITUDE: row[column_indices[consts_location_log.COLUMN_ALTITUDE]]
            })

        row_index += 1

    return locations


def write_location_to_log_file(log_file_abs_path: str, timestamp: str, latitude: str, longitude: str, altitude: str):
    _create_log_file_if_not_exists(log_file_abs_path)

    with open(log_file_abs_path, "a+", newline="") as log_file:
        log_file_writer = csv.writer(log_file)
        log_file_writer.writerow([str(timestamp), latitude, longitude, altitude])

    log_file.close()
