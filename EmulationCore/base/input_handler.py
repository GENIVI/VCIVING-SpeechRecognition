# This handles all the inputs and processes them as necessary.
import speech_recognition as SR
from ins.mechanisms.microphone import InputMicrophone
from threading import Thread
from outs.outs_mechanism import OutputMechanism
from base.input_processor import InputProcessor

# This is the default output mechanism used to output anything in the input processing section.

_default_output_mechanism : OutputMechanism = None
input_processor : InputProcessor = None


def ivi_init_inputs(default_output_mechanism, prediction_model_filepath, prediction_threshold, tasks_namespaces_folderpath):
    global _default_output_mechanism, input_processor
    _default_output_mechanism = default_output_mechanism

    input_processor = InputProcessor(ivi_output_via_default, prediction_model_filepath, prediction_threshold, tasks_namespaces_folderpath)

    # Initialize the Microphone
    ivi_init_microphone()


# Sets the default output mechanism used to output anything in the input processing section.
def ivi_set_default_output_mechanism(default_output_mechanism):
    global _default_output_mechanism
    _default_output_mechanism = default_output_mechanism


# Returns the default output mechanism used to output anything in the input processing section.
def ivi_get_default_output_mechanism() -> type(_default_output_mechanism):
    return _default_output_mechanism


def ivi_output_via_default(data, log=False):
    # Pauses the microphone just to prevent it from hearing itself.
    global _microphone_pause
    _microphone_pause = True
    _default_output_mechanism.write_data(data)
    _microphone_pause = False
    if log:
        print(data)


##
#  MICROPHONE
##

# The following variables defines the Microphone input behaviour
_microphone_input = None
# If following variable is set to True, the microphone exits its listening state.
# In order to re-state the microphone to listening state, call ivi_init_microphone()
_microphone_stop = False
# If the following variable is set to True, the microphone will stay calm and quiet, without listening to anything.
# But this would never make the microphone to leave its listening state, it just sits there are waits.
# In order to resume the action of the microphone, set this to True
_microphone_pause = False


# Microphone Methods
def ivi_init_microphone():
    global _microphone_stop

    _microphone_stop = False

    def _ivi_listener_run():
        global _microphone_input

        _microphone_input = InputMicrophone()
        ivi_output_via_default("Initialization successful. Waiting for Commands...", log=True)
        while not _microphone_stop:
            if not _microphone_pause:
                try:
                    spoken_str = _microphone_input.read_data()
                    print("Read from Microphone: " + spoken_str)
                    input_processor.process_data(InputProcessor.PROCESS_TYPE_MICROPHONE_DATA, spoken_str)

                except SR.UnknownValueError:
                    pass

                except SR.RequestError:
                    ivi_output_via_default("Google Cloud API Error.", log=True)

    listener_thread = Thread(target=_ivi_listener_run)
    listener_thread.daemon = True
    listener_thread.start()


def ivi_stop_microphone():
    global _microphone_stop
    _microphone_stop = True
    ivi_output_via_default("Microphone Listener Ended.", log=True)
# End of Microphone Methods.
