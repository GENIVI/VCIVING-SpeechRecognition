import multiprocessing
from GeoLocationProcess.locators.impl.iplocator import IPLocator
import commons.consts.queue as consts_queue
import commons.utils.queue as utils_queue
import time
from threading import Timer
import GeoLocationProcess.utils.locationlog as utils_location_log


def monitor_and_save_location(save_file_abs_path: str, record_intervals: int, queue_receive: multiprocessing.Queue, queue_send: multiprocessing.Queue):
    queue_send.put(consts_queue.PROCESS_FLAG_VALUE_SPAWNED)

    # We use IPLocator at the moment as we do not use the sensors up to now.
    locator = IPLocator()
    location_monitor_timer = None

    def exec_monitor_cycle():
        global location_monitor_timer

        location_timestamp = str(int(time.time()))
        location_latitude, location_longitude, location_altitude = locator.get_location()

        utils_location_log.write_location_to_log_file(save_file_abs_path, location_timestamp, location_latitude, location_longitude, location_altitude)

        location_monitor_timer = Timer(record_intervals, exec_monitor_cycle)
        location_monitor_timer.daemon = True
        location_monitor_timer.start()

    location_monitor_timer = Timer(record_intervals, exec_monitor_cycle)
    location_monitor_timer.daemon = True
    location_monitor_timer.start()

    process_destroy_flag: int = utils_queue.get_process_flag(queue_receive)
    while not process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_DESTROY:
        process_destroy_flag = utils_queue.get_process_flag(queue_receive)

        while process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_PAUSE:
            process_destroy_flag = utils_queue.get_process_flag(queue_receive)

            time.sleep(0.05)

        time.sleep(0.05)

    location_monitor_timer.cancel()
