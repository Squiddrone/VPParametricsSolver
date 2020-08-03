import argparse
from xml_analyzer import Calculator
from xml_analyzer import XMLReader


def evaluate_constraint_property(constraint_property_id: str, xmlreader: XMLReader) -> float:
    """
    Analyze parametrical diagram. Prerequisites:
    - "to"-end of the binding connectors must point to the constraint property
    - result property must contain the string "result" as initial value
    - constraint property must have stereotype analyzable
    - result must be noted at the left side of the "=" (i.e. C=A*B), the same
      applies to inequations (i.e. C<A*B)
    """
    # Create mapping between properties and values
    calculation_data = xmlreader.build_data_container(constraint_property_id)

    for dep in calculation_data.dependencies:
        dep_result = evaluate_constraint_property(dep.constraint_property_id, xmlreader)
        calculation_data.update_variable(dep.property, dep_result)

    # Feed _data to analyzer module
    calculator = Calculator(calculation_data)
    result = calculator.calculate()
    print(calculation_data.constraint_specification, calculation_data.result_property, ':', result)

    return result


def main():
    parser = argparse.ArgumentParser(description='Necessary startup parameters')
    parser.add_argument('--project_file_path')
    args = parser.parse_args()

    xmlreader = XMLReader(args.project_file_path)

    # Get all constraint property ids in a package as list
    cp_ids = xmlreader.find_constraint_property_ids()
    for cp_id in cp_ids:
        evaluate_constraint_property(cp_id, xmlreader)


if __name__ == "__main__":
    main()
