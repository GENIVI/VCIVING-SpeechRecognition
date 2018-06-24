from base import output_handler
from emucorebrain.core.predictor import Predictor
from emucorebrain.data.models.route_model import RouteModel

class InputProcessor:

    PROCESS_TYPE_MICROPHONE_DATA = 0

    OUTPUT_DATA_INTERPRET_FAILED = "Failed to recognize the command."

    def __init__(self, output_handler_namespace : output_handler, prediction_model_filepath, prediction_threshold, tasks_namespaces_folderpath):
        self._output_handler_namespace = output_handler_namespace
        self._predictor = Predictor(model_filepath=prediction_model_filepath, prediction_threshold=prediction_threshold)

        self._INIT_SUCCESS = False
        # This would automatically validate the namespaces inside.
        self._class_namespaces = self._predictor.get_loaded_namespaces(tasks_namespaces_folderpath)
        self._INIT_SUCCESS = True

    def process_data(self, process_type, data):
        if self._INIT_SUCCESS:
            if process_type == InputProcessor.PROCESS_TYPE_MICROPHONE_DATA:
                # Do the prediction and call the relevant class appropriately.
                prediction = self._predictor.predict_sentence(data)

                if not prediction is None:
                    prediction_model = RouteModel(prediction)

                    name_prediction_executor = prediction_model.get_name_task_executor()
                    prediction_executor = self._class_namespaces[name_prediction_executor]

                    prediction_method = prediction_model.get_executor_method_by_instance(prediction_executor)
                    prediction_method([data])

                    # prediction_executor = self._class_namespaces[prediction_executor_name]
                    # prediction_executor.run(data)
                else:
                    pass
                    # Output via the default output that given data cannot be interpreted
                    # Otherwise just return something from the function that would say the data cannot be interpreted.
                    # self._output_handler_namespace.output_via_mechanism(output_handler.default_output_mechanism, InputProcessor.OUTPUT_DATA_INTERPRET_FAILED, wait_until_completed=True, log=True)
            # Other process types goes here.
        else:
            raise Exception("Initialization has been failed.")
