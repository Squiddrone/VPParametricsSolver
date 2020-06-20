import collections
import xml.etree.ElementTree as Et


class XMLReader:
    def __init__(self, project_file):
        self._project_file = project_file
        self.tree = Et.parse(self._project_file)
        self.root = self.tree.getroot()

    def find_constraint_properties(self, package=""):
        return self.find_constraint_properties_in_package(package=package)

    def resolve_bindings(self, cp: Et.Element) -> list:
        query = ".//SysMLConstraintProperty[@Id='" + cp.get("Id") + "']//SysMLConstraintBlock"
        constraint_block = self.root.find(query)
        query = ".//SysMLConstraintBlock[@Id='" + constraint_block.get("Idref") + "']//Attribute"
        constraint_attributes = self.root.findall(query)
        query = ".//SysMLConstraintBlock[@Id='" + constraint_block.get("Idref") + "']" \
                                                                                  "//Attribute//SysMLBindingConnector"
        binding_connectors_refs = self.root.findall(query)
        binding_connectors = list()
        for ref in binding_connectors_refs:
            ref_id = ref.get('Idref')
            con = self.root.find(".//SysMLBindingConnector[@Id='" + ref_id + "']")
            binding_connectors.append(con)

        return binding_connectors

    def find_constraint_spec(self, cp: Et.Element) -> str:
        query = ".//ConstraintElement/ConstrainedElements//*[@Idref='" + cp.get("Id") + \
                "']/../..//CompositeValueSpecification"
        constraint_spec = self.root.find(query).get('Value')
        return constraint_spec

    def build_pv_map_list(self, cp: Et.Element) -> list:
        binding_connectors = self.resolve_bindings(cp)
        pv_map = collections.namedtuple('property_value_mapping', ['property', 'value'])
        pv_map_list = list()
        for bc in binding_connectors:
            id_from = bc.get('From')
            id_to = bc.get('To')
            val = self.root.find(".//Attribute[@Id='" + id_from + "']").get('InitialValue')
            prop = self.root.find(".//Attribute[@Id='" + id_to + "']").get('Name')
            m = pv_map(prop, val)
            pv_map_list.append(m)
        return pv_map_list

    def find_constraint_properties_in_package(self, stereotype: str = "", package: str = "") -> list:
        if package == "":
            query = ".//Package//SysMLBlock/ModelChildren/SysMLConstraintProperty/" \
                    "Stereotypes/Stereotype[@Name='analyzable']/../.."
        else:
            query = ".//Package[@Name='" + package + "']" \
                                                     "//SysMLBlock/ModelChildren/SysMLConstraintProperty/" \
                                                     "Stereotypes/Stereotype[@Name='analyzable']/../.."
        constraint_properties = self.root.findall(query)
        return constraint_properties