import importlib
from emucorebrain.data.abstracts.TaskExecutor import TaskExecutor


class RouteModel:

    INDEX_EXECUTOR = 0
    INDEX_METHOD = 1

    METHOD_SEPARATOR = '.'

    def __init__(self, route_str):
        self._route_str : str = route_str

    def get_name_task_executor(self):
        route_sep = self._route_str.split(self.METHOD_SEPARATOR)
        return route_sep[self.INDEX_EXECUTOR]

    # Please note that all the paths to the TaskExecutors namespaces should be added prior to calling this method.
    def get_task_executor(self):
        executor_name = self.get_name_executor_method()
        unique_class_import_name = executor_name + "." + executor_name
        class_namespace_class = getattr(importlib.import_module(unique_class_import_name), executor_name)
        class_namespace_instance = class_namespace_class()
        return class_namespace_instance

    def get_name_executor_method(self):
        route_sep = self._route_str.split(self.METHOD_SEPARATOR)
        if len(route_sep) > self.INDEX_METHOD:
            return route_sep[self.INDEX_METHOD]
        else:
            return TaskExecutor.DEFAULT_NAME_RUN_METHOD

    def get_executor_method(self):
        class_namespace_instance = self.get_task_executor()
        name_executor_method = self.get_name_executor_method()
        return getattr(class_namespace_instance, name_executor_method)

    def get_executor_method_by_instance(self, executor_instance : TaskExecutor):
        name_executor_method = self.get_name_executor_method()
        return getattr(executor_instance, name_executor_method)
