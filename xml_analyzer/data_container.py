import collections


class DataContainer:
    def __init__(self):
        self.mapping_element = collections.namedtuple('property_value_mapping', ['property', 'value'])
        self.mappings = dict()
        self.mappings['variables'] = dict()
        self.mappings['autocalc'] = dict()
        self.result_property = ''
        self.dependencies = list()
        self.constraint_specification = ''

    def add_prop_val_mapping(self, prop: str, value: str):
        self.mappings['variables'][prop] = float(value)

    def add_result_property(self, prop):
        self.result_property = prop

    def get_result_property(self) -> str:
        return self.result_property

    def add_dependency_mapping(self, prop: str):
        self.mappings['variables'][prop] = 'dep'

    def add_auto_calc_mapping(self, sysml_type_name: str, autocalc_method: str, values: list):
        try:
            map_elements = self.mappings['autocalc'][autocalc_method]
        except KeyError:
            map_elements = list()
        map_element = self.mapping_element(sysml_type_name, values)
        map_elements.append(map_element)
        self.mappings['autocalc'][autocalc_method] = map_elements

    def add_dependencies(self, dependencies: list):
        self.dependencies = dependencies

    def set_constraint_specification(self, constraint_spec: str):
        self.constraint_specification = constraint_spec

    def get_variable_names(self) -> list:
        return list(self.mappings['variables'].keys())

    def get_dependencies(self):
        return self.dependencies

    def update_variable(self, name: str, value: str):
        self.mappings['variables'][name] = value
