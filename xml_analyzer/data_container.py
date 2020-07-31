from enum import Enum
from .definitions import MappingElement


class DataContainerFields(Enum):
    variables = 'variables'
    autocalc = 'autocalc'


class DataContainer:
    def __init__(self):
        self._mapping_element = MappingElement
        self._mappings = dict()
        self._mappings[DataContainerFields.variables] = dict()
        self._mappings[DataContainerFields.autocalc] = dict()
        self._result_property = ''
        self._dependencies = list()
        self._constraint_specification = ''

    def add_prop_val_mapping(self, prop: str, value: str):
        self._mappings[DataContainerFields.variables][prop] = float(value)

    @property
    def mappings(self) -> dict:
        return self._mappings

    @property
    def result_property(self) -> str:
        return self._result_property

    @result_property.setter
    def result_property(self, prop):
        self._result_property = prop

    @property
    def constraint_specification(self):
        return self._constraint_specification

    @constraint_specification.setter
    def constraint_specification(self, constraint_spec: str):
        self._constraint_specification = constraint_spec

    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: list):
        self._dependencies = dependencies

    def add_dependency_mapping(self, prop: str):
        self._mappings[DataContainerFields.variables][prop] = 'dep'

    def add_auto_calc_mapping(self, sysml_type_name: str, autocalc_method: str, values: list):
        try:
            map_elements = self._mappings[DataContainerFields.autocalc][autocalc_method]
        except KeyError:
            map_elements = list()
        finally:
            map_element = self._mapping_element(sysml_type_name, values)
            map_elements.append(map_element)
            self._mappings[DataContainerFields.autocalc][autocalc_method] = map_elements

    def get_variable_names(self) -> list:
        return list(self._mappings[DataContainerFields.variables].keys())

    def update_variable(self, name: str, value: str):
        self._mappings[DataContainerFields.variables][name] = value
