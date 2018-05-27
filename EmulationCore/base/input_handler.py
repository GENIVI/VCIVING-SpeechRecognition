# This handles all the inputs and processes them as necessary.
import speech_recognition as SR
from ins.mechanisms.microphone import InputMicrophone
from threading import Thread
from outs.outs_mechanism import OutputMechanism

# This is the default output mechanism used to output anything in the input processing section.

_default_output_mechanism : OutputMechanism = None


def ivi_init_inputs(default_output_mechanism):
    global _default_output_mechanism
    _default_output_mechanism = default_output_mechanism

    # Initialize the Microphone
    ivi_init_microphone()


# Sets the default output mechanism used to output anything in the input processing section.
def ivi_set_default_output_mechanism(default_output_mechanism):
    global _default_output_mechanism
    _default_output_mechanism = default_output_mechanism


# Returns the default output mechanism used to output anything in the input processing section.
def ivi_get_default_output_mechanism() -> type(_default_output_mechanism):
    return _default_output_mechanism


def _ivi_output_via_default(data, log=False):
    # Error here
    # Engine Run Loop has already started thing.
    # _default_output_mechanism.write_data(data)
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


# Microphone Methods
def ivi_init_microphone():
    global _microphone_stop

    _microphone_stop = False

    def _ivi_listener_run():
        global _microphone_input

        _microphone_input = InputMicrophone()
        _ivi_output_via_default("Initialization successful. Waiting for Commands...", log=True)
        while not _microphone_stop:
            try:
                spoken_str = _microphone_input.read_data()
                _ivi_output_via_default("Read from Microphone: " + spoken_str, log=True)

            except SR.UnknownValueError:
                pass

            except SR.RequestError:
                _ivi_output_via_default("Google Cloud API Error.", log=True)

    listener_thread = Thread(target=_ivi_listener_run)
    listener_thread.daemon = True
    listener_thread.start()


def ivi_stop_microphone():
    global _microphone_stop
    _microphone_stop = True
    _ivi_output_via_default("Microphone Listener Ended.", log=True)
# End of Microphone Methods.
