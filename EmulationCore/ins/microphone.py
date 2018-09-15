# Microphone Input Mechanism
# Implements InputMechanism class

# We're currently using Speech Recognition Library from https://pypi.org/project/SpeechRecognition/
# Can be cloned from https://github.com/Uberi/speech_recognition
import speech_recognition as SR
from deepspeech.model import Model
import numpy as np
from threading import Thread
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, GrabberController
import time


class InputMicrophone(InputMechanism):

    CONTAINER_KEY = "ins_mechanism_microphone"

    SETTING_DS_FILE_PATH_MODEL = "sr_model_file_path"
    SETTING_DS_FILE_PATH_ALPHABET = "sr_alphabet_file_path"
    SETTING_DS_FILE_PATH_LM = "sr_lm_file_path"
    SETTING_DS_FILE_PATH_TRIE = "sr_trie_file_path"

    # Following time is the time which the thread should wait after one cycle of listening to microphone.
    # It is used to prevent microphone and the thread being overloaded with instructions and malfunctioning.
    # 1 second = 1000 milliseconds
    TIME_SLEEP_PER_CYCLE = 0.01

    # Constructor
    #
    # grabber_controller : The GrabberController instance containing all the Grabbers which are wrapped around various
    #               callback functions.
    #               The callback function to be called when the microphone hears some input from the user. This function
    #               should accept one string parameter and one Exception type parameter through which the heard text is
    #               passed into the callback function and through which the following listed errors are retrieved.
    #               If everything went fine and useful speech was recognized as text, the first parameter(string) will
    #               be set to the text data of the audio heard and the second parameter(Exception) will be None.
    #               If any exception occurs, first parameter(string) will be none and the second parameter(Exception)
    #               will be set to the exception occurred.
    def __init__(self, grabber_controller : GrabberController, ivi_settings : SettingsContainer):
        self._grabber_controller = grabber_controller

        # Create new Recognizer object which contains different calls to use different APIs
        ds_path_model = ivi_settings.get_setting(InputMicrophone.SETTING_DS_FILE_PATH_MODEL)
        ds_path_alphabet = ivi_settings.get_setting(InputMicrophone.SETTING_DS_FILE_PATH_ALPHABET)
        ds_path_lm = ivi_settings.get_setting(InputMicrophone.SETTING_DS_FILE_PATH_LM)
        ds_path_trie = ivi_settings.get_setting(InputMicrophone.SETTING_DS_FILE_PATH_TRIE)
        self._speech_recognizer = DeepSpeechRecognizer(ds_path_model, ds_path_alphabet, ds_path_lm, ds_path_trie)
        self._speech_microphone = SR.Microphone()

        self._speech_microphone_listening_state = False
        self._speech_last_heard_text = None

        def _recognize_audio_to_text(heard_speech):
            try:
                spoken_raw_text = self._speech_recognizer.recognize_ds(heard_speech)
                if self._speech_microphone_listening_state:
                    self._speech_last_heard_text = spoken_raw_text
                    grabber_controller.notify_grabbers(spoken_raw_text, None)

            except SR.UnknownValueError:
                grabber_controller.notify_grabbers(None, SR.UnknownValueError)

            except SR.RequestError:
                grabber_controller.notify_grabbers(None, SR.RequestError)

        def _recognize_speech_to_audio():
            with self._speech_microphone:
                heard_speech = self._speech_recognizer.listen(self._speech_microphone)

            _recognize_audio_to_text(heard_speech)

        self._system_alive = True

        def _exec_listener():
            while self._system_alive:
                _recognize_speech_to_audio()
                time.sleep(self.TIME_SLEEP_PER_CYCLE)

        listener_thread = Thread(target=_exec_listener)
        listener_thread.daemon = True
        listener_thread.start()

    # Starts listening on the microphone.
    def start_listening(self):
        self._speech_microphone_listening_state = True

    # Stops listening on the microphone
    def stop_listening(self, kill_permanently=False):
        self._speech_microphone_listening_state = False
        self._system_alive = not kill_permanently

    # Implementation of the read_data method of InputMechanism
    # Just returns the last heard text from the microphone.
    # Throws Exception if there was nothing heard.
    # Since microphone uses callback(interrupt) methods, this is not usually used.
    def read_data(self):
        if not self._speech_last_heard_text is None:
            return self._speech_last_heard_text
        else:
            raise Exception("Nothing has been heard by the microphone.")

    # Returns the associated GrabberController instance.
    def get_grabber_controller(self):
        return self._grabber_controller


class DeepSpeechRecognizer(SR.Recognizer):

    # Number of MFCC features to use
    N_FEATURES = 26
    # Size of the context window used for producing timesteps in the input vector
    N_CONTEXT = 9
    # Beam width used in the CTC decoder when building candidate transcriptions
    BEAM_WIDTH = 500
    # The alpha hyperparameter of the CTC decoder. Language Model weight
    LM_WEIGHT = 1.75
    # Valid word insertion weight. This is used to lessen the word insertion penalty
    # when the inserted word is part of the vocabulary
    VALID_WORD_COUNT_WEIGHT = 1.00

    # Default Sample Rate for transcribing audio.
    DEFAULT_SAMPLE_RATE = 16000

    def __init__(self, path_model: str, path_alphabet: str, path_lm: str, path_trie: str):
        super().__init__()

        self._model = Model(path_model, DeepSpeechRecognizer.N_FEATURES, DeepSpeechRecognizer.N_CONTEXT, path_alphabet, DeepSpeechRecognizer.BEAM_WIDTH)
        self._model.enableDecoderWithLM(path_alphabet, path_lm, path_trie, DeepSpeechRecognizer.LM_WEIGHT, DeepSpeechRecognizer.VALID_WORD_COUNT_WEIGHT, DeepSpeechRecognizer.VALID_WORD_COUNT_WEIGHT)

        self._sample_rate = DeepSpeechRecognizer.DEFAULT_SAMPLE_RATE

    def set_frame_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def recognize_ds(self, audio : SR.AudioData):
        audio_wav_data = audio.get_wav_data(convert_rate=self._sample_rate)
        audio_np_data = np.frombuffer(audio_wav_data, np.int16)
        recognized_text = self._model.stt(audio_np_data, self._sample_rate)

        if recognized_text is None or recognized_text == "":
            raise SR.UnknownValueError()
        else:
            return recognized_text
