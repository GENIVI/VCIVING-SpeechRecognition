import os, sys
import pip

from emucorebrain.consts import consts
import importlib
import json
import numpy as np
import emucorebrain.keywords.model as keywords_model
from emucorebrain.core.preprocessor import PreProcessor
from emucorebrain.core.trainer import Trainer
from emucorebrain.data.models.route_model import RouteModel


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

                self._classes = model_json[keywords_model.save_file_classes]
                self._word_list = model_json[keywords_model.save_file_words]
                self._synapse0 = np.asarray(model_json[keywords_model.save_file_synapse0])
                self._synapse1 = np.asarray(model_json[keywords_model.save_file_synapse1])

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

    @staticmethod
    def _is_task_executor(class_object):
        try:
            return class_object.VALID_TASK_EXECUTOR

        except AttributeError:
            return False

    @staticmethod
    def install_dependencies(list_deps : list):
        for dep in list_deps:
            args = ["-q"]
            pip.main(["install"] + args + [dep])

    def run_validation_on_namespace_dir(self, tasks_namespaces_folderpath):
        structure_definitions_filepath = tasks_namespaces_folderpath + "/" + consts.TASKS_STRUCT_FILE_FILENAME
        if os.path.exists(structure_definitions_filepath):
            dep_filepath = tasks_namespaces_folderpath + "/" + consts.TASKS_DEPS_FILE_FILENAME
            if os.path.exists(dep_filepath):
                dep_file = open(dep_filepath, "rb")
                dep_data = json.load(dep_file)

                list_dep_data = []
                for dep_index in dep_data:
                    dep_index_data = dep_data[dep_index]

                    if consts.TASKS_DEPS_FILE_PROP_DEP_NAME in dep_index_data and consts.TASKS_DEPS_FILE_PROP_DEP_VERSION in dep_index_data:
                        dep_index_name = dep_index_data[consts.TASKS_DEPS_FILE_PROP_DEP_NAME]
                        dep_index_version = dep_index_data[consts.TASKS_DEPS_FILE_PROP_DEP_VERSION]
                        dep_index_req_line = dep_index_name + "==" + dep_index_version

                        list_dep_data.append(dep_index_req_line)
                    else:
                        raise Exception("Dependencies file contains malformed(missing name/version) near the dependency index: " + dep_index)

                self.install_dependencies(list_dep_data)

                structure_definitions_file_data = open(structure_definitions_filepath).read()
                structure_definitions_file_data = json.loads(structure_definitions_file_data)

                if all(basic_prop in structure_definitions_file_data for basic_prop in consts.TASKS_STRUCT_FILE_BASIC_PROPERTY_KEYS):
                    sys.path.append(os.path.abspath(tasks_namespaces_folderpath))

                    executors = structure_definitions_file_data[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS]
                    for executor in executors:
                        executor_folder = executor[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_NAMESPACE]
                        executor_folder_path = tasks_namespaces_folderpath + "/" + executor_folder

                        if os.path.exists(executor_folder_path):
                            executor_route_model = RouteModel(executor[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_CLASS])
                            executor_name = executor_route_model.get_name_task_executor()
                            executor_file_name = executor_name + ".py"
                            executor_file_path = executor_folder_path + "/" + executor_file_name

                            if not os.path.exists(executor_file_path):
                                raise Exception("Class File: " + executor_name + " cannot be found inside the Namespace Folder: " + executor_folder + ".")
                            else:
                                # Each namespace(task) file should have its class with the same name as the file
                                try:
                                    sys.path.append(os.path.abspath(executor_folder_path))

                                    unique_class_import_name = executor_name + "." + executor_name
                                    unique_class_object = getattr(importlib.import_module(unique_class_import_name), executor_name)
                                    assert self._is_task_executor(unique_class_object)

                                except AssertionError:
                                    raise Exception("One of the namespaces in the tasks directory does not implement TaskExecutor.")

                                except Exception:
                                    raise Exception("Unexpected error. MAYBE the file(s) in the tasks directory you've provided contains ambiguous class names.")
                        else:
                            raise Exception("Namespace folder: " + executor_folder + " not found.")

                else:
                    raise Exception("One or more of the following required entries are not found in the " + consts.TASKS_STRUCT_FILE_FILENAME + ".\n" + consts.TASKS_STRUCT_FILE_PROP_DEP_DIRS + ", " + consts.TASKS_STRUCT_FILE_PROP_EXECUTORS)
            else:
                raise Exception("Namespace folder: " + tasks_namespaces_folderpath + " does not contain the dependencies folder: " + consts.TASKS_DEPS_FILE_FILENAME)
        else:
            raise Exception(consts.TASKS_STRUCT_FILE_FILENAME + " does not exist inside " + tasks_namespaces_folderpath +".\nPlease make sure the tasks executors folder path you've given contains valid TaskExecutors.")

    def get_loaded_namespaces(self, tasks_namespaces_folderpath):
        # If the validation occurs successfully, we get the sys.path appended with all the namespace directories and
        # the parent directory. Therefore it in not necessary to append them here again.
        self.run_validation_on_namespace_dir(tasks_namespaces_folderpath)

        class_namespaces = {}

        structure_definitions_filepath = tasks_namespaces_folderpath + "/" + consts.TASKS_STRUCT_FILE_FILENAME
        structure_definitions_file_data = open(structure_definitions_filepath).read()
        structure_definitions_file_data = json.loads(structure_definitions_file_data)
        executors = structure_definitions_file_data[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS]
        for executor in executors:
            executor_route_model = RouteModel(executor[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_CLASS])
            executor_name = executor_route_model.get_name_task_executor()

            unique_class_import_name = executor_name + "." + executor_name
            class_namespace_class = getattr(importlib.import_module(unique_class_import_name), executor_name)
            class_namespace_instance = class_namespace_class()
            class_namespaces[executor_name] = class_namespace_instance

        return class_namespaces
