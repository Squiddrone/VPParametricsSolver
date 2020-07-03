import parser
import xml.etree.ElementTree as Et
from enum import Enum
from .formula import Formula


class EquationTypes(Enum):
    equation = 'equation'
    inequation_gr_th = 'inequation_gr_th'
    inequation_sm_th = 'inequation_sm_th'
    inequation_gr_eq = 'inequation_gr_eq'
    inequation_sm_eq = 'inequation_sm_eq'


class Calculator:
    def __init__(self, constraint_property: Et.Element, property_value_mapping: dict, constraint_spec: str):
        self.constraint_property = constraint_property
        self.property_value_mapping = property_value_mapping
        self.constraint_spec = constraint_spec

    @staticmethod
    def get_expression_type(expr: str) -> [EquationTypes, str]:

        if '>=' in expr:
            expr_type = EquationTypes.inequation_gr_eq
            expr_sep = '>='
        elif '<=' in expr:
            expr_type = EquationTypes.inequation_sm_eq
            expr_sep = '<='
        elif '>' in expr:
            expr_type = EquationTypes.inequation_gr_th
            expr_sep = '>'
        elif '<' in expr:
            expr_type = EquationTypes.inequation_sm_th
            expr_sep = '<'
        elif '=' in expr:
            expr_type = EquationTypes.equation
            expr_sep = '='
        else:
            expr_type = 'undef'
            expr_sep = 'undef'

        return expr_type, expr_sep

    def resolve_auto_calc_function(self, autocalc_fcn, type_name):
        retval = None
        if autocalc_fcn == 'autosum':
            retval = self.do_autosum(type_name)

        if autocalc_fcn == 'automult':
            pass

        return retval

    def do_autosum(self, sysml_type_name):
        values = list()
        for value in self.property_value_mapping['autosum'][sysml_type_name]:
            values.append(value.value)
        return sum(values)

    def calculate_all(self):
        result_prop = ""

        expr_type, expr_sep = self.get_expression_type(self.constraint_spec)
        # code = parser.expr(self.constraint_spec.split(expr_sep)[1].strip()).compile()

        # if expr_type != EquationTypes.equation:
        #     result = eval(self.constraint_spec)
        #     print("Result for " + self.constraint_property.get('Name') + ": " + result_prop, str(result))
        #     print("Expression is of type " + expr_type.value)
        #     print("Expression: " + self.constraint_spec)
        #     print("LHS: ", eval(self.constraint_spec.split(expr_sep)[0]))
        #     print("RHS: ", str(eval(code)))
        # else:
        #     result = eval(code)
        #     print("Result for " + self.constraint_property.get('Name') + ": ", result_prop, "=", str(result))
        #     print("Expression is of type " + expr_type.value)
        #     print("Expression: " + self.constraint_spec)
        #     print("RHS: ", str(eval(code)))
        #
        # print("-------------------------------------------------------------------")
        return 0 # rückgabe unklar
