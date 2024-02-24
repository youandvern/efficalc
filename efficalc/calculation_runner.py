from typing import Callable

from efficalc import (
    Calculation,
    clear_all_input_default_overrides,
    get_all_calc_objects,
    reset_results,
    set_input_default_overrides,
)


class CalculationRunner(object):

    def __init__(self, calc_function: Callable, input_vals: dict[str, any] = None):
        self.calc_function = calc_function
        self.input_vals = input_vals if input_vals is not None else {}

    def calculate_all_items(self) -> list:
        clear_all_input_default_overrides()
        set_input_default_overrides(self.input_vals)
        reset_results()
        self.calc_function()
        return get_all_calc_objects()

    def calculate_results(self) -> list:
        all_calc_objects = self.calculate_all_items()
        return self.get_results_from_all_calc_items(all_calc_objects)

    @staticmethod
    def _is_result_object(ob) -> bool:
        if not isinstance(ob, Calculation):
            return False
        return ob.result_check

    @classmethod
    def get_results_from_all_calc_items(cls, all_items: list) -> list:
        return list(filter(cls._is_result_object, all_items))
