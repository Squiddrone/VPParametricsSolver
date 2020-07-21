from enum import Enum


class AutocalcMethods(Enum):
    autosum = 'autosum'


class EquationTypes(Enum):
    equation = 'equation'
    inequation_gr_th = 'inequation_gr_th'
    inequation_sm_th = 'inequation_sm_th'
    inequation_gr_eq = 'inequation_gr_eq'
    inequation_sm_eq = 'inequation_sm_eq'
