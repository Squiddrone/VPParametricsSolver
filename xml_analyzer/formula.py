from Equation import Expression
import numpy


class Formula:
    def __init__(self, constraint_spec: str = "", variables: list = []):
        self.expression = expression
        self.variables = variables

    def make_expression(self, expression: str):
        return Expression(self.expression, self.variables)


