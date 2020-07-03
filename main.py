from xml_analyzer import Calculator
from xml_analyzer import XMLReader
import argparse

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

    # Create mapping between properties and values
    property_value_mapping = xmlreader.build_property_value_map(constraint_property)

    for dep in property_value_mapping.get_dependencies():
        dep_result = do_calculation(dep.constraint_property_id, xmlreader)
        property_value_mapping.update_variable(dep.property, str(dep_result))

    # Feed data to analyzer module
    calculator = Calculator(constraint_property, property_value_mapping, cs_spec)
    result = calculator.calculate_all()

    return result


def main():
    parser = argparse.ArgumentParser(description='Necessary startup parameters')
    parser.add_argument('--project_file_path')
    args = parser.parse_args()

    xmlreader = XMLReader(args.project_file_path)

    # Get all constraint property ids in a package as list
    cp_ids_list = xmlreader.find_constraint_property_ids()
    for cp_id in cp_ids_list:
        do_calculation(cp_id, xmlreader)


if __name__ == "__main__":
    main()
