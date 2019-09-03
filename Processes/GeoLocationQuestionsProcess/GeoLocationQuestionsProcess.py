from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.processes.core import Process
import emucorebrain.keywords.process as keywords_process
import GeoLocationProcess.consts.settings as keywords_process_third_party
import GeoLocationQuestionsProcess.utils.locationlog as utils_locationlog
import GeoLocationQuestionsProcess.consts as consts_locationlog


# TODO: Start coding this process to ask questions based on the data we have in location history file.
# A location processor would be required to determine the journey of the user.
# Goal here is to ask questions about the journey or stopped location.
class GeoLocationQuestionsProcess(Process):

    def __init__(self):
        self._geolocation_save_abs_file_path: str = None

    def start_process(self, args):
        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]

        self._geolocation_save_abs_file_path = ivi_settings.get_setting(keywords_process_third_party.ARG_GEOLOCATION_SAVE_FILE_PATH)

    def exec_iter(self):
        locations = utils_locationlog.read_location_log(self._geolocation_save_abs_file_path)

    def resume_process(self):
        pass

    def pause_process(self):
        pass

    def destroy_process(self):
        pass
