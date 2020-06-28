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

    def resolve_bindings(self, cp: Et.Element) -> list:
        query = ".//SysMLConstraintProperty[@Id='{}']//SysMLConstraintBlock".format(cp.get("Id"))
        constraint_block = self.root.find(query)
        query = ".//SysMLConstraintBlock[@Id='{}']//Attribute".format(constraint_block.get("Idref"))
        constraint_attributes = self.root.findall(query)
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
        for bc in binding_connector_list:
            stereo = bc.find('./Stereotypes/Stereotype[@Name="external"]')
            if stereo is not None:
                id_from: str = bc.get('From')
                ref_attribute = self.root.find('.//*[@Id="{}"]'.format(id_from))
                ref_attribute_connectors = ref_attribute.iterfind('.//SysMLBindingConnector')
                for ra_con in ref_attribute_connectors:
                    if ra_con.get('Idref') != bc.get('Id'):
                        ref_constr_param_id = self.root.find(
                            './/*[@Id="{}"]'.format(ra_con.get('Idref'))
                        ).get('To')
                        ref_constr_block_id = self.root.find(
                            './/*[@Id="{}"]/../..'.format(ref_constr_param_id)
                        ).get('Id')
                        ref_constr_prop_id = self.root.find(
                            './/SysMLConstraintProperty//*[@Idref="{}"]/../..'.format(ref_constr_block_id)
                        ).get('Id')
                        property_name = self.root.find('.//*[@Id="{}"]'.format(bc.get('To'))).get('Name')
                        dependencies.append(dependency(property_name, ref_constr_prop_id))

        return dependencies

    def find_constraint_spec(self, cp: Et.Element) -> str:
        query = ".//ConstraintElement/ConstrainedElements//*[@Idref='{}']/../..//CompositeValueSpecification"\
            .format(cp.get("Id"))
        constraint_spec = self.root.find(query).get('Value')
        return constraint_spec

    def build_pv_map_dict(self, cp: Et.Element, types: list = None) -> dict:
        binding_connectors = self.resolve_bindings(cp)
        dependencies = self.resolve_dependencies(binding_connectors)

        pv_map = collections.namedtuple('property_value_mapping', ['property', 'value'])
        pv_map_dict = dict()
        pv_map_dict['noauto'] = dict()
        bc_dict = dict()
        for bc in binding_connectors:
            id_from = bc.get('From')
            id_to = bc.get('To')
            val = self.root.find(".//*[@Id='{}']".format(id_from)).get('InitialValue')
            prop = self.root.find(".//*[@Id='{}']".format(id_to)).get('Name')
            stereo = bc.find('./Stereotypes/Stereotype[@Name="external"]')
            if stereo is not None:
                val = 'dep'
            m = pv_map(prop, val)
            bc_dict[prop] = m

        pv_map_dict['noauto']['bc'] = bc_dict

        if types:
            pv_map_dict[types[0]] = dict()
            for t in types[1:]:
                auto_list = list()
                attribute = self.find_attributes(t)
                for a in attribute:
                    val = a.get('InitialValue')
                    prop = a.get('Name')
                    m = pv_map(prop, val)
                    auto_list.append(m)
                pv_map_dict[types[0]][t] = auto_list

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
        for cp in constraint_properties:
            constraint_property_ids.append(cp.get('Id'))

        return constraint_property_ids

    def find_constraint_property(self, val: str, method='by_id'):
        element = None
        if method == 'by_id':
            query = ".//SysMLConstraintProperty[@Id='{}']".format(val)
            element = self.root.find(query)

        return element
