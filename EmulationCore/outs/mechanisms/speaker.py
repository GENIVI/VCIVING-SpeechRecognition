# Speaker Output Mechanism
# Implements OutputMechanism class

# We're using pyttsx3 library, is open source. Can be cloned at https://github.com/nateshmbhat/pyttsx3
# pyttsx3 uses eSpeak Engine and pypiwin32 is another dependency.
import pyttsx3
from ..outs_mechanism import OutputMechanism


class OutputSpeaker(OutputMechanism):
    speaker_engine_prop_rate = "rate"

    # Constructor
    def __init__(self):
        self._speaker_engine = pyttsx3.init()
        self._data_queue = []

    # Read the speed at which the given text is spoken by the engine
    def get_speech_rate(self):
        return self._speaker_engine.getProperty(OutputSpeaker.speaker_engine_prop_rate)

    # Set the speed at which the given text is spoken by the engine
    def set_speech_rate(self, speech_rate):
        self._speaker_engine.setProperty(OutputSpeaker.speaker_engine_prop_rate, speech_rate)

    # Asks the Speaker to speak the given data.
    # data A String to be spoken through the speaker.
    # Set wait_to_finish to True if you need to wait to return until the speaker completes speaking, False otherwise.
    # No exceptions are thrown.
    def write_data(self, data):
        # Add to the queue
        self._data_queue.append(data)

    # This method is called by output_handler and should not be called elsewhere.
    # Speaks out all the data in the queue.
    def run_queued_data(self):
        # Ask the engine to speak
        for data in self._data_queue:
            self._speaker_engine.say(data)

        self._data_queue = []

        # Wait until the engine speaks
        self._speaker_engine.runAndWait()