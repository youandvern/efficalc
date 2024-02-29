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

    def __init__(self, calc_function: Callable, input_vals: dict[str, any] = None):
        self.calc_function = calc_function
        self.input_vals = input_vals if input_vals is not None else {}

    def calculate_all_items(self) -> list:
        clear_saved_objects()
        clear_all_input_default_overrides()

        set_input_default_overrides(self.input_vals)
        self.calc_function()
        all_calc_objects = get_all_calc_objects()

        clear_all_input_default_overrides()
        clear_saved_objects()
        return all_calc_objects

    def calculate_results(self) -> list:
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
