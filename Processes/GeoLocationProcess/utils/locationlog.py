import os
import csv
import GeoLocationProcess.consts.locationlog as consts_locationlog


def write_location_to_log_file(log_file_abs_path: str, timestamp: str, latitude: str, longitude: str, altitude: str):
    log_file_existed = os.path.isfile(log_file_abs_path)

    with open(log_file_abs_path, "a+", newline="") as log_file:
        log_file_writer = csv.writer(log_file)
        if not log_file_existed:
            log_file_writer.writerow([consts_locationlog.COLUMN_TIMESTAMP, consts_locationlog.COLUMN_LATITUDE, consts_locationlog.COLUMN_LONGITUDE, consts_locationlog.COLUMN_ALTITUDE])

        log_file_writer.writerow([str(timestamp), latitude, longitude, altitude])

    log_file.close()
