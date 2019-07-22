import pip
import sys, os
import emucorebrain.consts.consts as consts
import json
from emucorebrain.data.models.route_model import RouteModel
import importlib


# Installs the dependencies required.
def _install_dependencies(list_deps : list):
    for dep in list_deps:
        args = ["-q"]
        pip.main(["install"] + args + [dep])


# Checks whether the given class instance is a valid instance of the class Process.
def _is_valid_process(class_object):
    try:
        return class_object.VALID_PROCESS

    except AttributeError:
        return False


# Installs dependencies, Checks whether the given namespace directory for processes is valid.
def _run_validation_on_namespace_dir(processes_namespaces_folder_path):
    structure_definitions_file_path = processes_namespaces_folder_path + "/" + consts.PROCESSES_STRUCT_FILE_FILENAME
    if os.path.exists(structure_definitions_file_path):
        deps_file_path = processes_namespaces_folder_path + "/" + consts.PROCESSES_DEPS_FILE_FILENAME
        if os.path.exists(deps_file_path):
            deps_file = open(deps_file_path, "rb")
            deps_data = json.load(deps_file)

            list_dep_data = []
            for dep_index in deps_data:
                dep_index_data = deps_data[dep_index]

                if consts.PROCESSES_DEPS_FILE_PROP_DEP_NAME in dep_index_data and consts.PROCESSES_DEPS_FILE_PROP_DEP_VERSION in dep_index_data:
                    dep_index_name = dep_index_data[consts.PROCESSES_DEPS_FILE_PROP_DEP_NAME]
                    dep_index_version = dep_index_data[consts.PROCESSES_DEPS_FILE_PROP_DEP_VERSION]
                    dep_index_req_line = dep_index_name + "==" + dep_index_version

                    list_dep_data.append(dep_index_req_line)
                else:
                    raise Exception("Dependencies file contains malformed(missing name/version) near the dependency index: " + dep_index)

            _install_dependencies(list_dep_data)

            structure_definitions_file_data = open(structure_definitions_file_path).read()
            structure_definitions_file_data = json.loads(structure_definitions_file_data)

            if all(basic_prop in structure_definitions_file_data for basic_prop in consts.PROCESSES_STRUCT_FILE_BASIC_PROPERTY_KEYS):
                sys.path.append(os.path.abspath(processes_namespaces_folder_path))

                processes = structure_definitions_file_data[consts.PROCESSES_STRUCT_FILE_PROP_PROCESSES]
                for process in processes:
                    process_folder = process[consts.PROCESSES_STRUCT_FILE_PROP_PROCESSES_NAMESPACE]
                    process_folder_path = processes_namespaces_folder_path + "/" + process_folder

                    if os.path.exists(process_folder_path):
                        process_route_model = RouteModel(process[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_CLASS])
                        process_name = process_route_model.get_class_name()
                        process_file_name = process_name + ".py"
                        process_file_path = process_folder_path + "/" + process_file_name

                        if not os.path.exists(process_file_path):
                            raise Exception("Class File: " + process_name + " cannot be found inside the Namespace Folder: " + process_folder + ".")
                        else:
                            # Each namespace(task) file should have its class with the same name as the file
                            try:
                                sys.path.append(os.path.abspath(process_folder_path))

                                unique_class_import_name = process_name + "." + process_name
                                unique_class_object = getattr(importlib.import_module(unique_class_import_name), process_name)
                                assert _is_valid_process(unique_class_object)

                            except AssertionError:
                                raise Exception("One of the namespaces in the tasks directory does not implement Process.")

                            except Exception:
                                raise Exception("Unexpected error. MAYBE the file(s) in the tasks directory you've provided contains ambiguous class names.")
                    else:
                        raise Exception("Namespace folder: " + process_folder + " not found.")

            else:
                raise Exception("One or more of the following required entries are not found in the " + consts.PROCESSES_STRUCT_FILE_FILENAME + ".\n" + consts.PROCESSES_STRUCT_FILE_PROP_DEP_DIRS + ", " + consts.PROCESSES_STRUCT_FILE_PROP_PROCESSES)
        else:
            raise Exception("Namespace folder: " + processes_namespaces_folder_path + " does not contain the dependencies folder: " + consts.PROCESSES_DEPS_FILE_FILENAME)
    else:
        raise Exception(consts.PROCESSES_STRUCT_FILE_FILENAME + " does not exist inside " + processes_namespaces_folder_path + ".\nPlease make sure the processes folder path you've given contains valid implementations of Process interface.")


def get_loaded_namespaces(procceses_namespaces_folderpath):
    # If the validation occurs successfully, we get the sys.path appended with all the namespace directories and
    # the parent directory. Therefore it in not necessary to append them here again.
    _run_validation_on_namespace_dir(procceses_namespaces_folderpath)

    class_namespaces = []

    structure_definitions_file_path = procceses_namespaces_folderpath + "/" + consts.PROCESSES_STRUCT_FILE_FILENAME
    structure_definitions_file_data = open(structure_definitions_file_path).read()
    structure_definitions_file_data = json.loads(structure_definitions_file_data)
    processes = structure_definitions_file_data[consts.PROCESSES_STRUCT_FILE_PROP_PROCESSES]
    for process in processes:
        process_route_model = RouteModel(process[consts.PROCESSES_STRUCT_FILE_PROP_PROCESSES_CLASS])
        process_name = process_route_model.get_class_name()

        unique_class_import_name = process_name + "." + process_name
        class_namespace_class = getattr(importlib.import_module(unique_class_import_name), process_name)
        class_namespace_instance = class_namespace_class()
        class_namespaces.append(class_namespace_instance)

    return class_namespaces
