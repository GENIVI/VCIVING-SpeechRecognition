# This handles all the inputs and processes them as necessary.
import speech_recognition as SR
from base import output_handler
from ins.microphone import InputMicrophone
from base.input_processor import InputProcessor
from emucorebrain.data.containers.settings import SettingsContainer

# This is the default output mechanism used to output anything in the input processing section.

# Following variables defines all the input mechanisms here.
_microphone_input : InputMicrophone = None

_output_handler_namespace : output_handler = None
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
def ivi_init_inputs(output_handler_namespace : output_handler, ivi_settings : SettingsContainer):
    global _output_handler_namespace, input_processor, _microphone_input
    _output_handler_namespace = output_handler_namespace

    # Initializes the InputProcessor
    input_processor = InputProcessor(output_handler_namespace, ivi_settings)

    # Initialize the Microphone
    def _ivi_process_microphone_data(heard_text, exception):
        if exception is None:
            print("Read from Microphone: " + heard_text)
            input_processor.process_data(InputProcessor.PROCESS_TYPE_MICROPHONE_DATA, heard_text)
        else:
            if exception == SR.UnknownValueError:
                pass
            elif exception == SR.RequestError:
                output_handler_namespace.output_via_mechanism(mechanism=output_handler.default_output_mechanism, data="Google Cloud API Error. Could not interpret your speech.", wait_until_completed=True, log=True)
    _microphone_input = InputMicrophone(_ivi_process_microphone_data)
    _microphone_input.start_listening()


# Starts all the input mechanisms and asks them to grab the inputs.
def ivi_start_inputs():
    _microphone_input.start_listening()
    # Start all other input mechanisms


# Stops all the input mechanisms from grabbing the inputs.
def ivi_stop_inputs(kill_permanently=False):
    _microphone_input.stop_listening(kill_permanently=kill_permanently)
    # Stop all other input mechanisms
