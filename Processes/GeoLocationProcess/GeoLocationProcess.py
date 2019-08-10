import multiprocessing
import emucorebrain.keywords.process as keywords_process
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.processes.core import Process
import commons.consts.queue as consts_queue
import time
import GeoLocationProcess.geolocationsubprocess as geolocationsubprocess
import GeoLocationProcess.consts.settings as keywords_process_third_party


# The process to monitor and log the Geo-Location of the device.
class GeoLocationProcess(Process):

    def __init__(self):
        self._sub_process: multiprocessing.Process = None
        self._sub_process_queue_receive = multiprocessing.Queue()
        self._sub_process_queue_send = multiprocessing.Queue()

    # Since GeoLocation fetching and saving is a time consuming process, we do it in a separate thread.
    def start_process(self, args):
        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]

        geolocation_save_abs_file_path: str = ivi_settings.get_setting(keywords_process_third_party.ARG_GEOLOCATION_SAVE_FILE_PATH)
        geolocation_save_interval: int = int(ivi_settings.get_setting(keywords_process_third_party.ARG_GEOLOCATION_SAVE_INTERVAL))
        self._sub_process = multiprocessing.Process(target=geolocationsubprocess.monitor_and_save_location, args=(geolocation_save_abs_file_path, geolocation_save_interval, self._sub_process_queue_send, self._sub_process_queue_receive))
        self._sub_process.daemon = True
        self._sub_process.start()

        # Waits until the message is received that the process is spawned successfully.
        while not int(self._sub_process_queue_receive.get()) == consts_queue.PROCESS_FLAG_VALUE_SPAWNED:
            time.sleep(0.05)

    # There is nothing to be done manually at each iteration, this runs on a separate process with a timer and own resources, therefore just a pass
    def exec_iter(self):
        pass

    # Resumes monitoring the location.
    def resume_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_RUN)

    # Pauses monitoring the location.
    def pause_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_PAUSE)

    # Destroys and finishes the process.
    def destroy_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_DESTROY)
        self._sub_process.join()
