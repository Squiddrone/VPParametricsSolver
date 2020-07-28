import collections
import xml.etree.ElementTree as Et
from .data_container import DataContainer
from .definitions import AutocalcMethods


class XMLReader:

    def __init__(self, project_file):
        self._project_file = project_file
        self.tree = Et.parse(self._project_file)
        self.root = self.tree.getroot()

    @staticmethod
    def _parse_constraint_spec(constraint_spec: str) -> list:
        autocalc_sysml_type_name = list()
        for method in AutocalcMethods:
            if method.name in constraint_spec:
                autocalc_sysml_type_name.append(method.name)
                for occurrence in constraint_spec.split(method.name)[1:]:
                    search_param = occurrence[occurrence.find('(') + 1:occurrence.find(')')]
                    if search_param != '':
                        autocalc_sysml_type_name.append(search_param)
        return autocalc_sysml_type_name

    def _find_attributes(self, val: list, method='by_type'):
        elements = None
        if method == 'by_type':
            query = ".//Attribute/Type//*[@Name='{}']/../..".format(val)
            elements = self.root.findall(query)

        return elements

    def _resolve_bindings(self, constraint_property: Et.Element) -> list:
        query = ".//SysMLConstraintProperty[@Id='{}']//SysMLConstraintBlock".format(constraint_property.get("Id"))
        constraint_block = self.root.find(query)
        query = ".//SysMLConstraintBlock[@Id='{}']//Attribute//SysMLBindingConnector"\
            .format(constraint_block.get("Idref"))
        binding_connectors_refs = self.root.findall(query)
        binding_connectors = list()
        for ref in binding_connectors_refs:
            ref_id = ref.get('Idref')
            con = self.root.find(".//SysMLBindingConnector[@Id='{}']".format(ref_id))
            binding_connectors.append(con)

        return binding_connectors

    def _resolve_dependencies(self, binding_connectors: list) -> list:
        dependency = collections.namedtuple('dependency', ['property', 'constraint_property_id'])
        dependencies = list()
        for binding_connector in binding_connectors:
            stereo = binding_connector.find('./Stereotypes/Stereotype[@Name="external"]')
            if stereo is not None:
                id_from: str = binding_connector.get('From')
                ref_attribute = self.root.find('.//*[@Id="{}"]'.format(id_from))
                ref_attribute_connectors = ref_attribute.iterfind('.//SysMLBindingConnector')
                for ra_con in ref_attribute_connectors:
                    if ra_con.get('Idref') != binding_connector.get('Id'):
                        ref_constr_param_id = self.root.find(
                            './/*[@Id="{}"]'.format(ra_con.get('Idref'))
                        ).get('To')
                        ref_constr_block_id = self.root.find(
                            './/*[@Id="{}"]/../..'.format(ref_constr_param_id)
                        ).get('Id')
                        ref_constr_prop_id = self.root.find(
                            './/SysMLConstraintProperty//*[@Idref="{}"]/../..'.format(ref_constr_block_id)
                        ).get('Id')
                        property_name = self.root.find('.//*[@Id="{}"]'.format(binding_connector.get('To'))).get('Name')
                        dependencies.append(dependency(property_name, ref_constr_prop_id))

        return dependencies

    def _find_constraint_spec(self, constraint_property: Et.Element) -> str:
        query = ".//ConstraintElement/ConstrainedElements//*[@Idref='{}']/../..//CompositeValueSpecification"\
            .format(constraint_property.get("Id"))
        constraint_spec = self.root.find(query).get('Value')
        return constraint_spec

    def _find_constraint_property(self, val: str, method='by_id'):
        element = None
        if method == 'by_id':
            query = ".//SysMLConstraintProperty[@Id='{}']".format(val)
            element = self.root.find(query)

        return element

    def build_data_container(self, constraint_property_id: str) -> DataContainer:

        constraint_property = self._find_constraint_property(constraint_property_id)

        calculation_data = DataContainer()

        binding_connectors = self._resolve_bindings(constraint_property)
        dependencies = self._resolve_dependencies(binding_connectors)

        constraint_spec = self._find_constraint_spec(constraint_property)
        autocalc_sysml_type_names = self._parse_constraint_spec(constraint_spec)
        calculation_data.set_constraint_specification(constraint_spec)

        calculation_data.add_dependencies(dependencies)

        for binding_connector in binding_connectors:
            id_from = binding_connector.get('From')
            id_to = binding_connector.get('To')
            val = self.root.find(".//*[@Id='{}']".format(id_from)).get('InitialValue')
            prop = self.root.find(".//*[@Id='{}']".format(id_to)).get('Name')
            stereo = binding_connector.find('./Stereotypes/Stereotype[@Name="external"]')
            if stereo is not None:
                calculation_data.add_dependency_mapping(prop)
                continue
            if val != 'result':
                calculation_data.add_prop_val_mapping(prop, val)
            elif val == 'result':
                calculation_data.add_result_property(prop)

        if autocalc_sysml_type_names:
            for autocalc_sysml_type_name in autocalc_sysml_type_names[1:]:
                autocalc_values = list()
                attributes = self._find_attributes(autocalc_sysml_type_name)
                for attribute in attributes:
                    val = attribute.get('InitialValue')
                    autocalc_values.append(float(val))

                calculation_data.add_auto_calc_mapping(
                    autocalc_sysml_type_name,
                    autocalc_sysml_type_names[0],
                    autocalc_values
                )

        return calculation_data

    def find_constraint_property_ids(self, package: str = "") -> list:
        if package == "":
            query = ".//Package//SysMLBlock/ModelChildren/SysMLConstraintProperty/" \
                    "Stereotypes/Stereotype[@Name='analyzable']/../.."
        else:
            query = ".//Package[@Name='" + package + "']" \
                    "//SysMLBlock/ModelChildren/SysMLConstraintProperty/" \
                    "Stereotypes/Stereotype[@Name='analyzable']/../.."
        constraint_properties = self.root.findall(query)

        constraint_property_ids = list()
        for constraint_parameter in constraint_properties:
            constraint_property_ids.append(constraint_parameter.get('Id'))

        return constraint_property_ids
