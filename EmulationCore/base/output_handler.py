# This handles all the outputs and provides outputs as necessary
from base import input_handler
from outs.outs_mechanism import OutputMechanism
from outs.mechanisms.speaker import OutputSpeaker

# Following variable sets the default output mechanism used by the system.
# Defaults to OutputSpeaker instance when ivi_init_outputs is called.
default_output_mechanism : OutputMechanism = None

# Following variables defines all the output mechanisms here.
speaker_output : OutputSpeaker = None


# Initializes all the output mechanisms
def ivi_init_outputs():
    global speaker_output

    # Initialize the Speaker
    speaker_output = OutputSpeaker()
    # Update the speech rate to a more reasonable / understandable value when read.
    default_speech_rate = speaker_output.get_speech_rate()
    new_speech_rate = default_speech_rate - 50
    speaker_output.set_speech_rate(new_speech_rate)

    ivi_set_default_ouput_mechanism(speaker_output)


# General Methods

# Sets the default output mechanism
# mechanism: An implementation instance of the OutputMechanism class.
def ivi_set_default_ouput_mechanism(mechanism : OutputMechanism):
    global default_output_mechanism
    default_output_mechanism = mechanism


# Runs all the queued outputs in the OutputMechanisms defined above.
def ivi_run_outputs():
    speaker_output.run_queued_data()
    # Other outputs called here to output their queued data


# Used to output data from the system through the given mechanism
# mechanism: An implementation of the OutputMechanism which associates with a certain output device to output data.
# data: The data to output via the above mechanism. Usually a string but not a must.
# wait_until_completed: Specifies whether to return from the method before the output is completed.
def output_via_mechanism(mechanism: OutputMechanism, data, wait_until_completed=False, log=False):
    # Pauses the inputs just to prevent them from hearing the output from the system
    input_handler.ivi_stop_inputs()
    mechanism.write_data(data=data, wait_until_completed=wait_until_completed)
    # Restarts the inputs
    input_handler.ivi_start_inputs()

    if log:
        print(data)
