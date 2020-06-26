from XMLAnalyzer import analyzer as an
from XMLAnalyzer import xmlreader as xml

"""
Analyze parametrical diagram. Prerequisites:
- Constraint must be formulated in a python conformant way
- "to"-end of the binding connectors must point to the constraint property
- result property must contain the string "result" as initial value 
- constraint property must have stereotype analyzable
- result must be noted at the left side of the "=" (i.e. C=A*B), the same
  applies to inequations (i.e. C<A*B)
"""

project_file = '/home/cwild/devel/sq_dr_model_export/project.xml'

if __name__ == "__main__":
    xmlreader = xml.XMLReader(project_file)
    # Get all constraint properties in a package as list
    cp_list = xmlreader.find_constraint_properties()
    for cp in cp_list:
        # Get the constraint specification
        cs_spec = xmlreader.find_constraint_spec(cp)

        # Look for autosum expression
        search_param_list = xmlreader.parse_constraint_spec(cs_spec, 'autosum')

        # Create mapping between properties and values
        pv_map_dict = xmlreader.build_pv_map_dict(cp, search_param_list)

        # Feed data to analyzer module
        calc = an.Analyzer(cp=cp, pv_map_dict=pv_map_dict, cs_spec=cs_spec)
        calc.analyze_all()
