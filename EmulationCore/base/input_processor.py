from core.predictor import Predictor


class InputProcessor:

    PROCESS_TYPE_MICROPHONE_DATA = 0

    OUTPUT_DATA_INTERPRET_FAILED = "Failed to recognize the command."

    def __init__(self, ivi_output_via_default, prediction_model_filepath, prediction_threshold, tasks_namespaces_folderpath):
        self._ivi_output_via_default = ivi_output_via_default
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
                    # Output via the default output that given data cannot be interpreted
                    # Otherwise just return something from the function that would say the data cannot be interpreted.
                    self._ivi_output_via_default(InputProcessor.OUTPUT_DATA_INTERPRET_FAILED, log=True)
            # Other process types goes here.
        else:
            raise Exception("Initialization has been failed.")
