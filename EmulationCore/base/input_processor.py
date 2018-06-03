from base import output_handler
from core.predictor import Predictor


class InputProcessor:

    PROCESS_TYPE_MICROPHONE_DATA = 0

    OUTPUT_DATA_INTERPRET_FAILED = "Failed to recognize the command."

    def __init__(self, output_handler_namespace : output_handler, prediction_model_filepath, prediction_threshold, tasks_namespaces_folderpath):
        self._output_handler_namespace = output_handler_namespace
        self._predictor = Predictor(model_filepath=prediction_model_filepath, prediction_threshold=prediction_threshold)

        self._INIT_SUCCESS = self._predictor.run_validation_on_namespace_dir(tasks_namespaces_folderpath)
        self._class_namespaces = self._predictor.get_loaded_namespaces(tasks_namespaces_folderpath)

    def process_data(self, process_type, data):
        if self._INIT_SUCCESS:
            if process_type == InputProcessor.PROCESS_TYPE_MICROPHONE_DATA:
                # Do the prediction and call the relevant class appropriately.
                prediction = self._predictor.predict_sentence(data)
                if not prediction is None:
                    prediction_executor = self._class_namespaces[prediction]
                    prediction_executor.run(data)
                else:
                    pass
                    # Output via the default output that given data cannot be interpreted
                    # Otherwise just return something from the function that would say the data cannot be interpreted.
                    # self._output_handler_namespace.output_via_mechanism(output_handler.default_output_mechanism, InputProcessor.OUTPUT_DATA_INTERPRET_FAILED, wait_until_completed=True, log=True)
            # Other process types goes here.
        else:
            raise Exception("Initialization has been failed.")
