from latexexpr_efficalc import Expression, Operation, Variable

OPERATOR_TO_LATEX = {
    "<": "<",
    "<=": "\leq",
    "=": "=",
    "!=": r"\neq",
    "==": "=",
    ">": ">",
    ">=": "\geq",
}

_DEFAULT_OVERRIDE_KEY = "default_overrides"
_ALL_CALC_ITEMS_KEY = "all_calc_items"
_GLOBAL_STORE = {_DEFAULT_OVERRIDE_KEY: {}, _ALL_CALC_ITEMS_KEY: []}


class CalculationItem(object):
    super_type = "CalculationItem"


def save_calculation_item(item):
    _GLOBAL_STORE["all_calc_items"].append(item)


def get_override_or_default_value(input_name: str, default_value: any):
    default_overrides: dict = _GLOBAL_STORE[_DEFAULT_OVERRIDE_KEY]
    if default_overrides is not None and input_name in default_overrides:
        return default_overrides.get(input_name)
    else:
        return default_value


def clear_all_input_default_overrides() -> None:
    _GLOBAL_STORE[_DEFAULT_OVERRIDE_KEY] = {}


def set_input_default_overrides(default_overrides: dict[str, any]) -> None:
    _GLOBAL_STORE[_DEFAULT_OVERRIDE_KEY] = default_overrides


def reset_results() -> None:
    _GLOBAL_STORE[_ALL_CALC_ITEMS_KEY] = []


def get_all_calc_objects() -> list:
    return _GLOBAL_STORE[_ALL_CALC_ITEMS_KEY]


def _get_float_safe_operation(
    input_operation: Operation | Expression | Variable | float | int,
):
    if isinstance(input_operation, (float, int)):
        return Operation("", input_operation)
    else:
        return input_operation
