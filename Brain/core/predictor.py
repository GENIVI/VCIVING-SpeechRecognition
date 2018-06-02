import os,sys

import importlib
import json
import numpy as np
import keywords.model
from core.preprocessor import PreProcessor
from core.trainer import Trainer


class Predictor:

    ARG_KEY_MODEL_FILEPATH = "model_filepath"
    ARG_KEY_PREDICTION_THRESHOLD = "prediction_threshold"

    ARG_KEY_TRAINED_PREPROCESSOR = "trained_preprocessor"
    ARG_KEY_SYNAPSE0 = "synapse0"
    ARG_KEY_SYNAPSE1 = "synapse1"

    def __init__(self, *args, **dict_args):
        if len(dict_args) == 2:
            model_filepath = dict_args.get(self.ARG_KEY_MODEL_FILEPATH)
            prediction_threshold = dict_args.get(self.ARG_KEY_PREDICTION_THRESHOLD)

            with open(model_filepath, "r") as model_file:
                model_json = json.load(model_file)

                self._classes = model_json[keywords.model.save_file_classes]
                self._word_list = model_json[keywords.model.save_file_words]
                self._synapse0 = np.asarray(model_json[keywords.model.save_file_synapse0])
                self._synapse1 = np.asarray(model_json[keywords.model.save_file_synapse1])

            self._prediction_threshold = prediction_threshold

        elif len(dict_args) == 4:
            trained_preprocessor : PreProcessor = dict_args.get(self.ARG_KEY_TRAINED_PREPROCESSOR)
            synapse0 = dict_args.get(self.ARG_KEY_SYNAPSE0)
            synapse1 = dict_args.get(self.ARG_KEY_SYNAPSE1)
            prediction_threshold = dict_args.get(self.ARG_KEY_PREDICTION_THRESHOLD)

            self._classes = trained_preprocessor.get_unique_text_labels()
            self._word_list = trained_preprocessor.get_unique_wordlist()
            self._synapse0 = synapse0
            self._synapse1 = synapse1
            self._prediction_threshold = prediction_threshold

    def set_prediction_threshold(self, prediction_threshold):
        self._prediction_threshold = prediction_threshold

    def get_probable_classes_sentence(self, sentence):
        patternized_sentence = PreProcessor.get_sentence_patterns(sentence.lower(), self._word_list)

        # Input layer
        layer0 = patternized_sentence
        # Layer 1
        layer1 = Trainer.sigmoid(np.dot(layer0, self._synapse0))
        # Output layer
        layer2 = Trainer.sigmoid(np.dot(layer1, self._synapse1))

        results = [[i, probability] for i, probability in enumerate(layer2) if probability > self._prediction_threshold]
        results.sort(key=lambda x: x[1], reverse=True)
        return_results = [[self._classes[result[0]], result[1]] for result in results]

        return return_results

    def predict_sentence(self, sentence):
        probabilities = self.get_probable_classes_sentence(sentence)

        max_class = ""
        max_prob = 0

        for probability in probabilities:
            prob_class = probability[0]
            prob = probability[1]

            if prob > max_prob:
                max_class = prob_class
                max_prob = prob

        if max_prob > self._prediction_threshold:
            return max_class
        else:
            return None

    def get_unique_classes(self):
        return self._classes

    def _is_task_executor(self, class_object):
        try:
            return class_object.VALID_TASK_EXECUTOR

        except AttributeError:
            return False

    def run_validation_on_namespace_dir(self, tasks_namespaces_folderpath):
        sys.path.append(os.path.abspath(tasks_namespaces_folderpath))

        for unique_class in self.get_unique_classes():
            namespace_filepath = tasks_namespaces_folderpath + "/" + unique_class + ".py"
            if not os.path.exists(namespace_filepath):
                raise Exception("The tasks directory does not all the namespaces for classes in the model.")

            # Each namespace(task) file should have its class with the same name as the file
            try:
                unique_class_object = getattr(importlib.import_module(unique_class), unique_class)
                assert self._is_task_executor(unique_class_object)

            except AssertionError:
                raise Exception("One of the namespaces in the tasks directory does not implement TaskExecutor.")

            except Exception:
                raise Exception("Unexpected error. MAYBE the file(s) in the tasks directory you've provided contains ambiguous class names.")

        return True

    def get_loaded_namespaces(self, tasks_namespaces_folderpath):
        self.run_validation_on_namespace_dir(tasks_namespaces_folderpath)

        sys.path.append(os.path.abspath(tasks_namespaces_folderpath))

        class_namespaces = {}
        for unique_class in self.get_unique_classes():
            # Each namespace(task) file should have its class with the same name as the file
            class_namespace_class = getattr(importlib.import_module(unique_class), unique_class)
            class_namespace_instance = class_namespace_class()
            class_namespaces[unique_class] = class_namespace_instance

        return class_namespaces
