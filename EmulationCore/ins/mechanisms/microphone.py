# Microphone Input Mechanism
# Implements InputMechanism class

# We're currently using Speech Recognition Library from https://pypi.org/project/SpeechRecognition/
# Can be cloned from https://github.com/Uberi/speech_recognition
import speech_recognition as SR
from ..ins_mechanism import InputMechanism


class InputMicrophone(InputMechanism):
    # Constructor
    def __init__(self):
        # Create new Recognizer object which contains different calls to use different APIs
        self._speech_recognizer = SR.Recognizer()

    # Implementation of the read_data method of InputMechanism
    # Blocks the thread by which the method is called.
    # Returns a String of heard speech as text.
    # Raises SpeechRecognition.UnknownValueError on Failure to Hear useful information.
    # Raises SpeechRecognition.RequestError on Failure to retrieve information from Speech to Text Engine
    def read_data(self):
        # Wait until valid speech is heard.
        with SR.Microphone() as source:
            heard_speech = self._speech_recognizer.listen(source)

        try:
            spoken_raw_text = self._speech_recognizer.recognize_google(heard_speech)
            return spoken_raw_text

        except SR.UnknownValueError:
            # Failed to hear useful speech.
            raise

        except SR.RequestError:
            # Google API Error, maybe no internet connection.
            raise