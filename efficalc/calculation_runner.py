from typing import Callable

from efficalc import (
    Calculation,
    Comparison,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
    set_input_default_overrides,
)


class CalculationRunner(object):
    """A helper class for running calculation functions. It executes the provided calculation function and returns the
    calculation objects that were created during its execution. If input values are provided, they will override the
    default Input values.

    :param calc_function: The calculation function to be executed. This function should instantiate the relevant
                          calculation objects and perform the necessary calculations. The function is executed without
                          input parameters and returned values are ignored.
    :type calc_function: Callable
    :param input_vals: A dictionary of input values to override default values in the calculation function's Input objects.
                       Defaults to an empty dictionary if not provided.
    :type input_vals: dict[str, any], optional
    """

    def __init__(self, calc_function: Callable, input_vals: dict[str, any] = None):
        self.calc_function = calc_function
        self.input_vals = input_vals if input_vals is not None else {}

    def calculate_all_items(self) -> list:
        """
        Executes the calculation function and returns all calculation objects created during its execution (e.g.
        Assumption, Input, Calculation, Comparison, etc.). Ignores the calculation function return values.

        :return: A list of all calculation objects instantiated by the calculation function.
        :rtype: list
        """
        clear_saved_objects()
        clear_all_input_default_overrides()

        set_input_default_overrides(self.input_vals)
        self.calc_function()
        all_calc_objects = get_all_calc_objects()

        clear_all_input_default_overrides()
        clear_saved_objects()
        return all_calc_objects

    def calculate_results(self) -> list:
        """
        Executes the calculation function and filters the results to return only those Calculation and Comparison
        objects that have been marked as results (where result_check=True).

        :return: A list of calculation objects where result_check=True.
        :rtype: list
        """
        all_calc_objects = self.calculate_all_items()
        return self._get_results_from_all_calc_items(all_calc_objects)

    @staticmethod
    def _is_calculated_result(ob) -> bool:
        if not isinstance(ob, Calculation) and not isinstance(ob, Comparison):
            return False
        return ob.result_check

    @classmethod
    def _get_results_from_all_calc_items(cls, all_items: list) -> list:
        return list(filter(cls._is_calculated_result, all_items))
