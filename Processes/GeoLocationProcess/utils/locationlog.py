import os
import csv


def write_location_to_log_file(log_file_abs_path: str, timestamp: str, latitude: str, longitude: str):
    log_file_existed = os.path.isfile(log_file_abs_path)

    with open(log_file_abs_path, "a+", newline="") as log_file:
        log_file_writer = csv.writer(log_file)
        if not log_file_existed:
            log_file_writer.writerow(["Timestamp", "Latitude", "Longitude"])

        log_file_writer.writerow([str(timestamp), latitude, longitude])

    log_file.close()
