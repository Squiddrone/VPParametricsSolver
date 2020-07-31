from Equation import Expression
from .definitions import EquationTypes


class Formula(Expression):
    def __init__(self, constraint_spec: str = "", variables: list = None):
        self._expression = self._make_expression(constraint_spec)
        super().__init__(self._expression, variables)

    def _make_expression(self, expression: str):
        expr_type, expr_sep = self._get_expression_type(expression)
        if expr_type == EquationTypes.equation:
            expression = expression.split(expr_sep)[1]
        return expression

    @staticmethod
    def _get_expression_type(expr: str) -> [EquationTypes, str]:
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
