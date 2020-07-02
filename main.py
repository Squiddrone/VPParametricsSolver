from xml_analyzer import Calculator
from xml_analyzer import XMLReader
import argparse # use to fill the PROJECT_FILE variale via console parameter

"""
Analyze parametrical diagram. Prerequisites:
- Constraint must be formulated in a python conformant way
- "to"-end of the binding connectors must point to the constraint property
- result property must contain the string "result" as initial value
- constraint property must have stereotype analyzable
- result must be noted at the left side of the "=" (i.e. C=A*B), the same
  applies to inequations (i.e. C<A*B)
"""

PROJECT_FILE = ''

def do_calculation(constraint_property_id: str, xmlreader: XMLReader) -> str:
    constraint_property = xmlreader.find_constraint_property(constraint_property_id)
    # Get the constraint specification
    cs_spec = xmlreader.find_constraint_spec(constraint_property)

    # Look for autosum expression
    search_param_list = xmlreader.parse_constraint_spec(cs_spec, 'autosum')

    # Create mapping between properties and values
    property_value_mapping = xmlreader.build_pv_map_dict(constraint_property, search_param_list)

    for dep in property_value_mapping['dependencies']:
        dep_result = do_calculation(dep.constraint_property_id)
        property_value_mapping['noauto']['bc'][dep.property] = xmlreader.pv_map(dep.property, str(dep_result))

    # Feed data to analyzer module
    calculator = Calculator(constraint_property, property_value_mapping, cs_spec)
    result = calculator.calculate_all()

    return result

def main():
    xmlreader = XMLReader(PROJECT_FILE)

    # Get all constraint property ids in a package as list
    cp_ids_list = xmlreader.find_constraint_property_ids()
    for cp_id in cp_ids_list:
        do_calculation(cp_id)

if __name__ == "__main__":
    main()
