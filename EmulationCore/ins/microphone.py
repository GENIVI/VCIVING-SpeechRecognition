# Microphone Input Mechanism
# Implements InputMechanism class

# We're currently using Speech Recognition Library from https://pypi.org/project/SpeechRecognition/
# Can be cloned from https://github.com/Uberi/speech_recognition
import speech_recognition as SR
from threading import Thread
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism
import time


class InputMicrophone(InputMechanism):

    # Following time is the time which the thread should wait after one cycle of listening to microphone.
    # It is used to prevent microphone and the thread being overloaded with instructions and malfunctioning.
    # 1 second = 1000 milliseconds
    TIME_SLEEP_PER_CYCLE = 0.01

    # Constructor
    # on_listen :   The callback function to be called when the microphone hears some input from the user. This function
    #               should accept one string parameter and one Exception type parameter through which the heard text is
    #               passed into the callback function and through which the following listed errors are retrieved.
    #               If everything went fine and useful speech was recognized as text, the first parameter(string) will
    #               be set to the text data of the audio heard and the second parameter(Exception) will be None.
    #               If any exception occurs, first parameter(string) will be none and the second parameter(Exception)
    #               will be set to the exception occurred.
    def __init__(self, on_listen):
        # Create new Recognizer object which contains different calls to use different APIs
        self._speech_recognizer = SR.Recognizer()
        self._speech_microphone = SR.Microphone()

        self._speech_microphone_listening_state = False
        self._speech_last_heard_text = None

        def _recognize_audio_to_text(heard_speech):
            try:
                spoken_raw_text = self._speech_recognizer.recognize_google(heard_speech)
                if self._speech_microphone_listening_state:
                    self._speech_last_heard_text = spoken_raw_text
                    on_listen(spoken_raw_text, None)

            except SR.UnknownValueError:
                on_listen(None, SR.UnknownValueError)

            except SR.RequestError:
                on_listen(None, SR.RequestError)

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
