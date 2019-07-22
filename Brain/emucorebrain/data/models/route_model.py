import importlib


class RouteModel:

    INDEX_CLASS = 0
    INDEX_METHOD = 1

    METHOD_SEPARATOR = '.'
    DEFAULT_NAME_RUN_METHOD = "run"

    def __init__(self, route_str):
        self._route_str: str = route_str

    def get_class_name(self):
        route_sep = self._route_str.split(self.METHOD_SEPARATOR)
        return route_sep[self.INDEX_CLASS]

    def get_method_name(self):
        route_sep = self._route_str.split(self.METHOD_SEPARATOR)
        if len(route_sep) > self.INDEX_METHOD:
            return route_sep[self.INDEX_METHOD]
        else:
            return RouteModel.DEFAULT_NAME_RUN_METHOD

    # Please note that all the paths to the Class namespaces should be added prior to calling this method.
    def get_class_instance(self):
        class_name = self.get_method_name()
        unique_class_import_name = class_name + "." + class_name
        class_namespace_class = getattr(importlib.import_module(unique_class_import_name), class_name)
        class_namespace_instance = class_namespace_class()
        return class_namespace_instance

    def get_method(self):
        class_namespace_instance = self.get_class_instance()
        name_method = self.get_method_name()
        return getattr(class_namespace_instance, name_method)

    def get_method_by_class_instance(self, class_instance):
        name_method = self.get_method_name()
        return getattr(class_instance, name_method)
