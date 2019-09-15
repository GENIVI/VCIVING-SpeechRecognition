from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.containers.lockers import LockersContainer
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.models.lockers import LockerTypes
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, GrabberController, Grabber
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from emucorebrain.processes.core import Process
import emucorebrain.keywords.process as keywords_process
import GeoLocationProcess.consts.settings as keywords_process_third_party
from commons.locations.analyzers import GeoLocationLogAnalyzer
import commons.locations.log.consts.locationlog as consts_location_log
import GeoLocationQuestionsProcess.consts.ins_mechanisms as consts_ins_mechanisms
import speech_recognition as SR


# A locations processor would be required to determine the journey of the user.
# Goal here is to ask questions about the journey or stopped locations.
class GeoLocationQuestionsProcess(Process):

    def __init__(self):
        self._geo_location_save_abs_file_path: str = None
        self._geo_location_analyzer: GeoLocationLogAnalyzer = None

        self._last_cluster = 0

        self._lockers: LockersContainer = None
        self._default_ins_mechanism: InputMechanism = None
        self._default_outs_mechanism: OutputMechanism = None

        self._paused = False

    def start_process(self, args):
        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]

        self._geo_location_save_abs_file_path = ivi_settings.get_setting(keywords_process_third_party.ARG_GEOLOCATION_SAVE_FILE_PATH)
        self._geo_location_analyzer = GeoLocationLogAnalyzer(log_file_path=self._geo_location_save_abs_file_path, location_update_interval=int(ivi_settings.get_setting(keywords_process_third_party.ARG_GEOLOCATION_SAVE_INTERVAL)))

        self._lockers = args[keywords_process.ARG_LOCKERS_CONTAINER]

        ivi_ins_mechanisms_carriers = args[keywords_process.ARG_INS_MECHANISMS_CARRIERS]
        ivi_ins_mechanism_carrier_default: OutputMechanismCarrier = ivi_ins_mechanisms_carriers[keywords_process.ARG_INS_MECHANISMS_MECHANISM_DEFAULT]
        self._default_ins_mechanism = ivi_ins_mechanism_carrier_default.get_data()

        ivi_outs_mechanisms_carriers = args[keywords_process.ARG_OUTS_MECHANISMS_CARRIERS]
        ivi_outs_mechanism_carrier_default: OutputMechanismCarrier = ivi_outs_mechanisms_carriers[keywords_process.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT]
        self._default_outs_mechanism = ivi_outs_mechanism_carrier_default.get_data()

    def exec_iter(self):
        if not self._paused and not self._lockers.is_inputs_locked():
            # Reloads data from the files.
            self._geo_location_analyzer.refresh_data()

            if self._geo_location_analyzer.get_locations_count() > 1:
                locations_with_clusters = self._geo_location_analyzer.get_location_clusters()
                latest_location_cluster = locations_with_clusters[len(locations_with_clusters) - 1][consts_location_log.COLUMN_CLUSTER]

                if latest_location_cluster != self._last_cluster:
                    if self._geo_location_analyzer.is_a_stop_cluster(cluster=self._last_cluster, location_clusters=locations_with_clusters):
                        locker_id_ins_mechanisms = self._lockers.add_locker(LockerTypes.INPUT_MECHANISMS)
                        locker_id_outs_mechanisms = self._lockers.add_locker(LockerTypes.OUTPUT_MECHANISMS)

                        self._default_outs_mechanism.write_data("Where did you stopped by?", wait_until_completed=True)

                        def ins_default_mechanism_grab_answer(*args, ivi_ins_mechanism_default=self._default_ins_mechanism, ivi_outs_mechanism_default=self._default_outs_mechanism, ivi_lockers=self._lockers):
                            if ivi_ins_mechanism_default.CONTAINER_KEY == consts_ins_mechanisms.CONTAINER_KEY_INPUT_MICROPHONE:
                                # If Default Input Mechanism is InputMicrophone
                                heard_text = args[0]
                                exception = args[1]

                                if exception is None:
                                    print("Read from Microphone: " + heard_text)
                                    ivi_outs_mechanism_default.write_data("OK! I will remember that", wait_until_completed=True)

                                    # TODO: Remember what's being said.
                                else:
                                    if exception == SR.UnknownValueError:
                                        return
                                    elif exception == SR.RequestError:
                                        ivi_outs_mechanism_default.write_data("Google Cloud API Error. Could not interpret your speech.", wait_until_completed=True)

                                ins_default_mechanism_grabber_controller.pop_out_grabber(GrabberController.MAX_PRIORITY_INDEX)

                                ivi_lockers.remove_locker(locker_id_ins_mechanisms)
                                ivi_lockers.remove_locker(locker_id_outs_mechanisms)

                        ins_default_mechanism_grabber_controller: GrabberController = self._default_ins_mechanism.get_grabber_controller()
                        ins_default_mechanism_grabber_controller.pop_in_grabber(Grabber(ins_default_mechanism_grab_answer), GrabberController.MAX_PRIORITY_INDEX)

                    self._last_cluster = latest_location_cluster

    def resume_process(self):
        self._paused = False

    def pause_process(self):
        self._paused = True

    def destroy_process(self):
        self._geo_location_save_abs_file_path = None
        self._geo_location_analyzer = None
