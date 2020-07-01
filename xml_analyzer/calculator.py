import parser
import xml.etree.ElementTree as Et
from enum import Enum


class EquationTypes(Enum):
    equation = 'equation'
    inequation_gr_th = 'inequation_gr_th'
    inequation_sm_th = 'inequation_sm_th'
    inequation_gr_eq = 'inequation_gr_eq'
    inequation_sm_eq = 'inequation_sm_eq'


class Calculator:
    def __init__(self, cp: Et.Element, pv_map_dict: dict, cs_spec: str):
        self.constraint_property = cp
        self.pv_map_dict = pv_map_dict
        self.cs_spec = cs_spec

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

    def calculate_all(self):
        result_prop = ""
        for key in self.pv_map_dict.keys():
            if key == 'noauto':
                for entry in self.pv_map_dict[key]['bc'].values():
                    if entry.value != 'result':
                        exec(entry.property + "=" + entry.value)
                    elif entry.value == 'result':
                        result_prop = entry.property
            elif key == 'autosum':
                for entry in self.pv_map_dict[key]:
                    exec(entry + "=0")
                    for val in self.pv_map_dict[key][entry]:
                        exec(entry + "+=" + val.value)
                    self.cs_spec = self.cs_spec.replace(key + '(' + entry + ')', entry)

        expr_type, expr_sep = self.get_expression_type(self.cs_spec)
        code = parser.expr(self.cs_spec.split(expr_sep)[1].strip()).compile()

        if expr_type != EquationTypes.equation:
            result = eval(self.cs_spec)
            print("Result for " + self.constraint_property.get('Name') + ": " + result_prop, str(result))
            print("Expression is of type " + expr_type.value)
            print("Expression: " + self.cs_spec)
            print("LHS: ", eval(self.cs_spec.split(expr_sep)[0]))
            print("RHS: ", str(eval(code)))
        else:
            result = eval(code)
            print("Result for " + self.constraint_property.get('Name') + ": ", result_prop, "=", str(result))
            print("Expression is of type " + expr_type.value)
            print("Expression: " + self.cs_spec)
            print("RHS: ", str(eval(code)))

        print("-------------------------------------------------------------------")
        return result
