import multiprocessing
from emucorebrain.processes.core import Process
import emucorebrain.keywords.process as keywords_process
from emucorebrain.data.containers.settings import SettingsContainer
import UniversalModelTrainerProcess.universalmodeltrainersubprocess as universalmodeltrainersubprocess
import commons.consts.queue as consts_queue
import time


class UniversalModelTrainerProcess(Process):

    def __init__(self):
        self._sub_process: multiprocessing.Process = None
        self._sub_process_queue_receive = multiprocessing.Queue()
        self._sub_process_queue_send = multiprocessing.Queue()

    def start_process(self, args):
        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]

        self._sub_process = multiprocessing.Process(target=universalmodeltrainersubprocess.trigger_training, args=(ivi_settings, self._sub_process_queue_send, self._sub_process_queue_receive))
        self._sub_process.daemon = True
        self._sub_process.start()

        # Waits until the message is received that the process is spawned successfully.
        while not int(self._sub_process_queue_receive.get()) == consts_queue.PROCESS_FLAG_VALUE_SPAWNED:
            time.sleep(0.05)

    # There is nothing to be done manually at each iteration, this runs on a separate process with a timer and own resources, therefore just a pass
    def exec_iter(self):
        pass

    # Resumes monitoring the locations.
    def resume_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_RUN)

    # Pauses monitoring the locations.
    def pause_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_PAUSE)

    # Destroys and finishes the process.
    def destroy_process(self):
        self._sub_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_DESTROY)
        self._sub_process.join()
