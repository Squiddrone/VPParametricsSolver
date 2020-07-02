import collections
import xml.etree.ElementTree as Et


class XMLReader:
    def __init__(self, project_file):
        self._project_file = project_file
        self.tree = Et.parse(self._project_file)
        self.root = self.tree.getroot()
        self.pv_map = collections.namedtuple('property_value_mapping', ['property', 'value'])

    @staticmethod
    def parse_constraint_spec(cspec: str, fcntype: str = "") -> list:
        searchparam_list = list()

        if fcntype in cspec:
            searchparam_list.append(fcntype)
            for occurrence in cspec.split(fcntype)[1:]:
                search_param = occurrence[occurrence.find('(') + 1:occurrence.find(')')]
                if search_param != '':
                    searchparam_list.append(search_param)
        return searchparam_list

    def find_attributes(self, val: list, method='by_type'):
        elements = None
        if method == 'by_type':
            query = ".//Attribute/Type//*[@Name='{}']/../..".format(val)
            elements = self.root.findall(query)

        return elements

    def resolve_bindings(self, constraint_property: Et.Element) -> list:
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

    def resolve_dependencies(self, binding_connector_list: list) -> list:
        dependency = collections.namedtuple('dependency', ['property', 'constraint_property_id'])
        dependencies = list()
        for binding_connector in binding_connector_list:
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

    def find_constraint_spec(self, constraint_property: Et.Element) -> str:
        query = ".//ConstraintElement/ConstrainedElements//*[@Idref='{}']/../..//CompositeValueSpecification"\
            .format(constraint_property.get("Id"))
        constraint_spec = self.root.find(query).get('Value')
        return constraint_spec

    def build_pv_map_dict(self, constraint_property: Et.Element, attribute_types: list = None) -> dict:
        binding_connectors = self.resolve_bindings(constraint_property)
        dependencies = self.resolve_dependencies(binding_connectors)

        pv_map = collections.namedtuple('property_value_mapping', ['property', 'value'])
        pv_map_dict = dict()
        pv_map_dict['noauto'] = dict()
        bc_dict = dict()
        for binding_connector in binding_connectors:
            id_from = binding_connector.get('From')
            id_to = binding_connector.get('To')
            val = self.root.find(".//*[@Id='{}']".format(id_from)).get('InitialValue')
            prop = self.root.find(".//*[@Id='{}']".format(id_to)).get('Name')
            stereo = binding_connector.find('./Stereotypes/Stereotype[@Name="external"]')
            if stereo is not None:
                val = 'dep'
            bc_dict[prop] = pv_map(prop, val)

        pv_map_dict['noauto']['bc'] = bc_dict

        if attribute_types:
            pv_map_dict[attribute_types[0]] = dict()
            for attribute_type in attribute_types[1:]:
                auto_list = list()
                attributes = self.find_attributes(attribute_type)
                for attribute in attributes:
                    val = attribute.get('InitialValue')
                    prop = attribute.get('Name')
                    auto_list.append(pv_map(prop, val))
                pv_map_dict[attribute_types[0]][attribute_type] = auto_list

        pv_map_dict['dependencies'] = dependencies

        return pv_map_dict

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

    def find_constraint_property(self, val: str, method='by_id'):
        element = None
        if method == 'by_id':
            query = ".//SysMLConstraintProperty[@Id='{}']".format(val)
            element = self.root.find(query)

        return element