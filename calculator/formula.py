from Equation import Expression
from definitions import EquationTypes


class Formula(Expression):
    def __init__(self, constraint_spec: str = "", variables: list = None):
        self._expression = self._make_expression(constraint_spec)
        super().__init__(self._expression, variables)

    def _make_expression(self, expression: str):
        equation_type, math_symbol = self._get_equation_type(expression)
        if equation_type == EquationTypes.equation:
            expression = expression.split(math_symbol)[1]
        return expression

    @staticmethod
    def _get_equation_type(math_expression: str) -> [EquationTypes, str]:
        if '>=' in math_expression:
            equation_type = EquationTypes.inequation_gr_eq
            math_symbol = '>='
        elif '<=' in math_expression:
            equation_type = EquationTypes.inequation_sm_eq
            math_symbol = '<='
        elif '>' in math_expression:
            equation_type = EquationTypes.inequation_gr_th
            math_symbol = '>'
        elif '<' in math_expression:
            equation_type = EquationTypes.inequation_sm_th
            math_symbol = '<'
        elif '=' in math_expression:
            equation_type = EquationTypes.equation
            math_symbol = '='
        else:
            equation_type = 'undef'
            math_symbol = 'undef'

        return equation_type, math_symbol
