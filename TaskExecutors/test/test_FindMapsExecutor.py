from emucorebrain.data.carriers.ins_mechanism import InputMechanismCarrier
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.carriers.string import StringCarrier
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from FindMapsExecutor.FindMapsExecutor import FindMapsExecutor
import emucorebrain.keywords.task_executor as keywords_task_executor

map_finder : FindMapsExecutor = FindMapsExecutor()

class TempInputMechanism(InputMechanism):

    def start_listening(self):
        pass

    def stop_listening(self, raise_exception_if_stopped=True):
        pass

    def read_data(self):
        pass

    def get_grabber_controller(self):
        pass

class TempOutputMechanism(OutputMechanism):

    def write_data(self, data, wait_until_completed=False):
        pass

    def run_queued_data(self):
        pass


def find_location_in_sentence(sentence):
    global map_finder

    ivi_settings = SettingsContainer("D:/Dev/GENIVI/Projects/EmulationCore/settings.json")
    ivi_input_mechanisms_carriers = {
        keywords_task_executor.ARG_INS_MECHANISMS_MECHANISM_DEFAULT: InputMechanismCarrier(TempInputMechanism())
    }
    ivi_output_mechanisms_carriers = {
        keywords_task_executor.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT: OutputMechanismCarrier(TempOutputMechanism())
    }

    args = {
        keywords_task_executor.ARG_SPEECH_TEXT_DATA: StringCarrier(sentence),
        keywords_task_executor.ARG_SETTINGS_CONTAINER: ivi_settings,
        keywords_task_executor.ARG_INS_MECHANISMS_CARRIERS: ivi_input_mechanisms_carriers,
        keywords_task_executor.ARG_OUTS_MECHANISMS_CARRIERS: ivi_output_mechanisms_carriers
    }

    map_finder.run(args)


find_location_in_sentence("find me the city of california")
