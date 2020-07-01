from xml_analyzer import calculator as calc
from xml_analyzer import xmlreader as xml

"""
Analyze parametrical diagram. Prerequisites:
- Constraint must be formulated in a python conformant way
- "to"-end of the binding connectors must point to the constraint property
- result property must contain the string "result" as initial value
- constraint property must have stereotype analyzable
- result must be noted at the left side of the "=" (i.e. C=A*B), the same
  applies to inequations (i.e. C<A*B)
"""

PROJECT_FILE = '/home/cwild/devel/sq_dr_model_export/project.xml'

if __name__ == "__main__":
    xmlreader = xml.XMLReader(PROJECT_FILE)

    # Get all constraint property ids in a package as list
    cp_ids_list = xmlreader.find_constraint_property_ids()
    for cp_id in cp_ids_list:

        def do_calculation(constraint_property_id):
            constraint_property = xmlreader.find_constraint_property(constraint_property_id)
            # Get the constraint specification
            cs_spec = xmlreader.find_constraint_spec(constraint_property)

            # Look for autosum expression
            search_param_list = xmlreader.parse_constraint_spec(cs_spec, 'autosum')

            # Create mapping between properties and values
            pv_map_dict = xmlreader.build_pv_map_dict(constraint_property, search_param_list)

            for dep in pv_map_dict['dependencies']:
                dep_result = do_calculation(dep.constraint_property_id)
                pv_map_dict['noauto']['bc'][dep.property] = xmlreader.pv_map(dep.property, str(dep_result))

            # Feed data to analyzer module
            calculator = calc.Calculator(cp=constraint_property, pv_map_dict=pv_map_dict, cs_spec=cs_spec)
            result = calculator.calculate_all()

            return result

        do_calculation(cp_id)
