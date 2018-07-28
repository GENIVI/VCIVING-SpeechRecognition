from emucorebrain.data.carriers.ins_mechanism import InputMechanismCarrier
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.carriers.string import StringCarrier
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from FindMapsExecutor.FindMapsExecutor import FindMapsExecutor
import emucorebrain.keywords.task_executor as keywords_task_executor

map_finder : FindMapsExecutor = FindMapsExecutor()


def find_location_in_sentence(sentence):
    global map_finder

    ivi_settings = SettingsContainer("D:/GENIVI/Projects/EmulationCore/settings.json")
    ivi_input_mechanisms_carriers = {
        keywords_task_executor.ARG_INS_MECHANISMS_MECHANISM_DEFAULT: InputMechanismCarrier(None)
    }
    ivi_output_mechanisms_carriers = {
        keywords_task_executor.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT: OutputMechanismCarrier(None)
    }

    args = {
        keywords_task_executor.ARG_SPEECH_TEXT_DATA: StringCarrier(sentence),
        keywords_task_executor.ARG_SETTINGS_CONTAINER: ivi_settings,
        keywords_task_executor.ARG_INS_MECHANISMS_CARRIERS: ivi_input_mechanisms_carriers,
        keywords_task_executor.ARG_OUTS_MECHANISMS_CARRIERS: ivi_output_mechanisms_carriers
    }

    map_finder.run(args)


find_location_in_sentence("Concord")
