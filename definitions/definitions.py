from enum import Enum
from collections import namedtuple

MappingElement = namedtuple('property_value_mapping', ['property', 'value'])


class AutocalcMethods(Enum):
    autosum = 'autosum'


class EquationTypes(Enum):
    equation = 'equation'
    inequation_gr_th = 'inequation_gr_th'
    inequation_sm_th = 'inequation_sm_th'
    inequation_gr_eq = 'inequation_gr_eq'
    inequation_sm_eq = 'inequation_sm_eq'
