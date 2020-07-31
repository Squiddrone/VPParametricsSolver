from .data_container import DataContainer, DataContainerFields
from .formula import Formula


class Calculator:
    def __init__(self, data: DataContainer):
        self.data = data
        self.formula = Formula(data.constraint_specification, data.get_variable_names())

    @staticmethod
    def _resolve_auto_calc_functions(autocalc_method, values):
        if autocalc_method == 'autosum':
            return round(sum(values), 3)
        return None

    def calculate(self) -> float:
        for autocalc_method in self.data.mappings[DataContainerFields.autocalc]:
            for autocalc_entry in self.data.mappings[DataContainerFields.autocalc][autocalc_method]:
                sysml_type_name = autocalc_entry.property
                auto_value = self._resolve_auto_calc_functions(autocalc_method, autocalc_entry.value)
                self.data.add_prop_val_mapping(sysml_type_name, str(auto_value))

        result = self.formula(*list(self.data.mappings[DataContainerFields.variables].values()))
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

        return result
