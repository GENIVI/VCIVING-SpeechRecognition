# This handles all the processes and executes the tasks as necessary.
from emucorebrain.data.carriers.ins_mechanism import InputMechanismCarrier
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.containers.lockers import LockersContainer
import base.consts.processes as consts_processes
import emucorebrain.processes.namespace as processes_namespace
from typing import List
from threading import Thread
import time
from emucorebrain.processes.core import Process
import emucorebrain.keywords.process as keywords_process
import utils.mechanisms
from base import input_handler
from base import output_handler

# Holder for all the processes
_processes: List[Process] = None
_thread_processes: Thread = None
_ivi_shutdown = False

# Initializes all the processes.
def init_processes(ivi_settings: SettingsContainer, ivi_lockers: LockersContainer):
    global _processes, _thread_processes

    processes_namespaces_folder_path = ivi_settings.get_setting(consts_processes.SETTINGS_PROCESSES_NAMESPACE_FOLDER_PATH)
    _processes = processes_namespace.get_loaded_namespaces(processes_namespaces_folder_path)

    args = {
        keywords_process.ARG_SETTINGS_CONTAINER: ivi_settings,
        keywords_process.ARG_LOCKERS_CONTAINER: ivi_lockers,
        keywords_process.ARG_INS_MECHANISMS_CARRIERS: {
            keywords_process.ARG_INS_MECHANISMS_MECHANISM_DEFAULT: InputMechanismCarrier(input_handler.default_input_mechanism),
            **utils.mechanisms.get_carries_by_mechanisms(InputMechanismCarrier.CARRIER_TYPE, input_handler.ivi_get_ins_mechanisms())
        },
        keywords_process.ARG_OUTS_MECHANISMS_CARRIERS: {
            keywords_process.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT: OutputMechanismCarrier(output_handler.default_output_mechanism),
            **utils.mechanisms.get_carries_by_mechanisms(OutputMechanismCarrier.CARRIER_TYPE, output_handler.ivi_get_outs_mechanisms())
        }
    }

    for process in _processes:
        process.start_process(args)


# Starts running the processes until the system shuts down.
def start_processes():
    global _thread_processes

    def exec_processes():
        while not _ivi_shutdown:
            for process in _processes:
                process.exec_iter()
            time.sleep(0.05)

    _thread_processes = Thread(target=exec_processes)
    _thread_processes.daemon = True
    _thread_processes.start()


# Stops/Destroys all the processes permanently
def destroy_processes():
    global _ivi_shutdown
    _ivi_shutdown = True

    for process in _processes:
        process.destroy_process()


