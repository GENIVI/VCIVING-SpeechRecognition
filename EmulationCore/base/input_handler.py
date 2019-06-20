# This handles all the inputs and processes them as necessary.
import speech_recognition as SR
from base import output_handler
from ins.microphone import InputMicrophone
from base.input_processor import InputProcessor
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, Grabber, GrabberController

# This is the default output mechanism used to output anything in the input processing section.

# Following variable sets the default input mechanism used by the system.
# Defaults to InputMicrophone instance when ivi_init_inputs is called.
default_input_mechanism : InputMechanism = None

# Following variables defines all the input mechanisms here.
microphone_input : InputMicrophone = None

input_processor : InputProcessor = None


# Initializes all the input mechanisms
# output_handler_namespace: The namespace of completely initialized output_handler.py
# prediction_model_filepath:   The path to the file(model) which is used to interpret the user inputs
#                               (natural language inputs)
# prediction_threshold: The value at which a certain interpretation(prediction) done through the model is accepted as
#                       as correct prediction even though it is the highest among others. This value lies within 0 and 1
#                       i.e. 0.0 <= prediction_threshold <= 1.0
#                       This is a float value.
# tasks_namespaces_folderpath:  The path to the folder containing all the classes implementing the tasks given by the
#                               predictions of the model. Head over to /Brain/data/abstracts/TasksExecutor.py for more
#                               documentation.
def ivi_init_inputs(ivi_settings: SettingsContainer):
    global input_processor, microphone_input

    # Initializes the InputProcessor
    input_processor = InputProcessor(ivi_settings)

    # Initialize the Microphone
    def _ivi_process_microphone_data(heard_text, exception):
        if exception is None:
            print("Read from Microphone: " + heard_text)
            input_processor.process_data(InputProcessor.PROCESS_TYPE_MICROPHONE_DATA, heard_text)
        else:
            if exception == SR.UnknownValueError:
                pass
            elif exception == SR.RequestError:
                output_handler.output_via_mechanism(mechanism=output_handler.default_output_mechanism,
                                                    data="Google Cloud API Error. Could not interpret your speech.",
                                                    wait_until_completed=True, log=True)
    # Initialize the Grabbers and GrabberControllers
    grabbers_list = [Grabber(_ivi_process_microphone_data)]
    grabber_controller = GrabberController(grabber_list=grabbers_list, notify_all=False)
    microphone_input = InputMicrophone(ivi_settings=ivi_settings, grabber_controller=grabber_controller)
    microphone_input.start_listening()

    ivi_set_default_input_mechanism(microphone_input)

# Sets the default input mechanism
# mechanism: An implementation instance of the InputMechanism class.
def ivi_set_default_input_mechanism(mechanism : InputMechanism):
    global default_input_mechanism
    default_input_mechanism = mechanism

# Starts all the input mechanisms and asks them to grab the inputs.
def ivi_start_inputs():
    microphone_input.start_listening()
    # Start all other input mechanisms


# Stops all the input mechanisms from grabbing the inputs.
def ivi_stop_inputs(kill_permanently=False):
    microphone_input.stop_listening(kill_permanently=kill_permanently)
    # Stop all other input mechanisms

def ivi_get_ins_mechanisms():
    return {
        InputMicrophone.CONTAINER_KEY: microphone_input,
        # Add all other input mechanisms here.
    }
