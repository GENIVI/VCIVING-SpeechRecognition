from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.containers.lockers import LockersContainer
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.models.lockers import LockerTypes
from emucorebrain.processes.core import Process
import emucorebrain.keywords.process as keywords_process
import EavesdropProcess.consts.settings as keywords_process_third_party
import multiprocessing
import commons.consts.queue as consts_queue
import EavesdropProcess.eavesdropsubprocess as eavesdropsubprocess
import time


# This process listens to user's every other conversation, records and stores them for betting to know the user better.
# Additionally this may transcribe the audio and save it together with the audio file.
class EavesdropProcess(Process):

    # Declaration of the variables.
    def __init__(self):
        self._is_valid_process = False
        self._audio_file_time = 0
        self._save_folder_path: str = None
        self._py_process_queue_receive = multiprocessing.Queue()
        self._py_process_queue_send = multiprocessing.Queue()

        self._process: multiprocessing.Process = None

    # Spawns a process to record the microphone, seamlessly in the background and save with the given time interval.
    # The process created here would be communicated with the aid of a queue.
    # The created is destroyed when the EmulationCore shuts down.
    def start_process(self, args):
        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]
        ivi_lockers: LockersContainer = args[keywords_process.ARG_LOCKERS_CONTAINER]
        ivi_outs_mechanisms_carriers = args[keywords_process.ARG_OUTS_MECHANISMS_CARRIERS]
        ivi_outs_mechanism_carrier_default: OutputMechanismCarrier = ivi_outs_mechanisms_carriers[keywords_process.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT]
        default_outs_mechanism = ivi_outs_mechanism_carrier_default.get_data()

        eavesdrop_mode_status = int(ivi_settings.get_setting(keywords_process_third_party.ARG_EAVESDROP_MODE_STATUS))
        self._is_valid_process = True if eavesdrop_mode_status == keywords_process_third_party.VALUE_EAVESDROP_MODE_STATUS_ALLOWED else False

        if self._is_valid_process:
            self._audio_file_time = int(ivi_settings.get_setting(keywords_process_third_party.ARG_EAVESDROP_MODE_SAVE_INTERVAL))
            self._save_folder_path = ivi_settings.get_setting(keywords_process_third_party.ARG_EAVESDROP_MODE_SAVE_FOLDER_PATH)

            self._process = multiprocessing.Process(target=eavesdropsubprocess.capture_and_save_audio, args=(self._audio_file_time, self._save_folder_path, self._py_process_queue_send, self._py_process_queue_receive))
            self._process.daemon = True
            self._process.start()

            # Waits until the message is received that the process is spawned successfully.
            while not int(self._py_process_queue_receive.get()) == consts_queue.PROCESS_FLAG_VALUE_SPAWNED:
                time.sleep(0.05)
        elif eavesdrop_mode_status != keywords_process_third_party.VALUE_EAVESDROP_MODE_STATUS_ALLOWED and eavesdrop_mode_status != keywords_process_third_party.VALUE_EAVESDROP_MODE_STATUS_NOT_ALLOWED:
            locker_id_outs_mechanisms = ivi_lockers.add_locker(LockerTypes.OUTPUT_MECHANISMS)
            default_outs_mechanism.write_data("You have not changed permissions for record user's speech as audio. Please change the permissions before next run.")
            ivi_lockers.remove_locker(locker_id_outs_mechanisms)

    # Nothing to be done in here as everything runs in a separate process.
    def exec_iter(self):
        pass

    # Resumes recording the audio
    def resume_process(self):
        if self._is_valid_process:
            self._py_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_RUN)

    # Pauses recording the audio
    def pause_process(self):
        if self._is_valid_process:
            self._py_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_PAUSE)

    # Destroys and Finishes the Process
    def destroy_process(self):
        if self._is_valid_process:
            self._py_process_queue_send.put(consts_queue.PROCESS_FLAG_VALUE_DESTROY)
            self._process.join()
