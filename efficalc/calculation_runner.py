from typing import Callable, Dict, List, Literal, Union, overload

from efficalc import (
    Calculation,
    Comparison,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
    set_input_default_overrides,
    Symbolic,
)

ResultType = Union[Calculation, Comparison]


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

    @overload
    def calculate_results(self, return_type: Literal["list"]) -> List[ResultType]: ...

    @overload
    def calculate_results(
        self, return_type: Literal["dict"]
    ) -> Dict[str, ResultType]: ...

    def calculate_results(
        self, return_type: Literal["list", "dict"] = "list"
    ) -> Union[List[ResultType], Dict[str, ResultType]]:
        """
        Executes the calculation function and filters the results to return only those Calculation and Comparison
        objects that have been marked as results (where result_check=True), either in a list or a dictionary format
        based on the 'return_type' parameter.

        :param return_type: The type of the return value, "list" for a list of calculation objects,
                            "dict" for a dictionary of calculation objects with their names as keys, defaults to "list"
        :type: return_type: "list" or "dict", optional
        :return: A list or a dictionary of calculation objects where result_check=True.
        """
        all_calc_objects = self.calculate_all_items()

        if return_type == "list":
            return list(filter(self._is_calculated_result, all_calc_objects))
        elif return_type == "dict":
            return {
                item.name: item
                for item in all_calc_objects
                if self._is_calculated_result(item)
            }
        else:
            raise ValueError("Invalid return_type specified. Use 'list' or 'dict'.")

    @staticmethod
    def _is_calculated_result(ob) -> bool:
        if (
            not isinstance(ob, Calculation)
            and not isinstance(ob, Comparison)
            and not isinstance(ob, Symbolic)
        ):
            return False
        return ob.result_check
