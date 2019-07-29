from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.containers.lockers import LockersContainer
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.models.lockers import LockerTypes
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, GrabberController, Grabber
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from emucorebrain.processes.core import Process
import RandomQuestionsProcess.consts.settings as keywords_process_third_party
import emucorebrain.keywords.process as keywords_process
from threading import Timer
import random
import RandomQuestionsProcess.consts.ins_mechanisms as consts_ins_mechanisms
import speech_recognition as SR


# This process would be temporary, would ask questions from a user on regular time intervals.
class RandomQuestionsProcess(Process):

    TEMP_RANDOM_QUESTIONS = [
        "Hey, What is your name?",
        "Are you currently driving?",
        "What is your favorite coffee shop?"
    ]

    def __init__(self):
        self._interval_timer = None
        self._timer: Timer = None
        self._timer_done = False
        self._timer_paused = False

        self._lockers: LockersContainer = None
        self._default_ins_mechanism: InputMechanism = None
        self._default_outs_mechanism: OutputMechanism = None

    # Marks whether the timer has completed the countdown.
    def _set_timer_state(self, state: bool):
        self._timer_done = state

    # Initializes and starts the timer for countdown.
    def _init_start_timer(self):
        self._set_timer_state(False)
        self._timer = Timer(self._interval_timer, self._set_timer_state, [True])
        self._timer.start()

    def start_process(self, args):
        self._lockers = args[keywords_process.ARG_LOCKERS_CONTAINER]

        ivi_ins_mechanisms_carriers = args[keywords_process.ARG_INS_MECHANISMS_CARRIERS]
        ivi_ins_mechanism_carrier_default: OutputMechanismCarrier = ivi_ins_mechanisms_carriers[keywords_process.ARG_INS_MECHANISMS_MECHANISM_DEFAULT]
        self._default_ins_mechanism = ivi_ins_mechanism_carrier_default.get_data()

        ivi_outs_mechanisms_carriers = args[keywords_process.ARG_OUTS_MECHANISMS_CARRIERS]
        ivi_outs_mechanism_carrier_default: OutputMechanismCarrier = ivi_outs_mechanisms_carriers[keywords_process.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT]
        self._default_outs_mechanism = ivi_outs_mechanism_carrier_default.get_data()

        ivi_settings: SettingsContainer = args[keywords_process.ARG_SETTINGS_CONTAINER]
        self._interval_timer = int(ivi_settings.get_setting(keywords_process_third_party.QUESTION_IMPOSE_TIME_INTERVAL))
        self._init_start_timer()

    def exec_iter(self):
        if not self._lockers.is_inputs_locked() and not self._lockers.is_outputs_locked():
            if self._timer_done:
                locker_id_ins_mechanisms = self._lockers.add_locker(LockerTypes.INPUT_MECHANISMS)
                locker_id_outs_mechanisms = self._lockers.add_locker(LockerTypes.OUTPUT_MECHANISMS)

                self._default_outs_mechanism.write_data("We have a question for you. Let me ask.", wait_until_completed=True)
                random_question_index = random.randint(0, len(RandomQuestionsProcess.TEMP_RANDOM_QUESTIONS) - 1)
                random_question = RandomQuestionsProcess.TEMP_RANDOM_QUESTIONS[random_question_index]
                self._default_outs_mechanism.write_data(random_question, wait_until_completed=True)

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

                self._init_start_timer()
        else:
            self._timer.cancel()
            self._init_start_timer()

    def resume_process(self):
        if self._timer_paused:
            self._init_start_timer()

            self._timer_paused = False

    def pause_process(self):
        if not self._timer_paused:
            self._set_timer_state(False)
            self._timer.cancel()

            self._timer_paused = True

    def destroy_process(self):
        self._set_timer_state(False)
        self._timer.cancel()
        self._timer: Timer = None
        self._timer_paused = False

        self._default_outs_mechanism = None

