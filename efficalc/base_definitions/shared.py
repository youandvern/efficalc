import threading

from latexexpr_efficalc import Expression, Operation, Variable

OPERATOR_TO_LATEX = {
    "<": "<",
    "<=": r"\leq",
    "=": "=",
    "!=": r"\neq",
    "==": "=",
    ">": ">",
    ">=": r"\geq",
}

_DEFAULT_OVERRIDE_KEY = "default_overrides"
_ALL_CALC_ITEMS_KEY = "all_calc_items"
_THREAD_LOCAL_STORE = threading.local()


class CalculationItem(object):
    """A base class for all calculation items. Not currently used for anything yet."""

    super_type = "CalculationItem"


def _get_thread_local_store():

    if not hasattr(_THREAD_LOCAL_STORE, "efficalc_store"):
        _THREAD_LOCAL_STORE.efficalc_store = {
            _DEFAULT_OVERRIDE_KEY: {},
            _ALL_CALC_ITEMS_KEY: [],
        }

    return _THREAD_LOCAL_STORE.efficalc_store


def save_calculation_item(item):
    """Save an item to the global store of all calculation items."""
    _get_thread_local_store()[_ALL_CALC_ITEMS_KEY].append(item)


def clear_saved_objects():
    """Clear all saved calculation items from the global store."""
    _get_thread_local_store()[_ALL_CALC_ITEMS_KEY] = []


def get_override_or_default_value(input_name: str, default_value: any):
    """Get the default override value for a given input name from the global store. If no override is found, returns
    the default value."""
    default_overrides: dict = _get_thread_local_store()[_DEFAULT_OVERRIDE_KEY]
    if default_overrides is not None and input_name in default_overrides:
        return default_overrides.get(input_name)
    else:
        return default_value


def set_input_default_overrides(default_overrides: dict[str, any]):
    """Set default override values for input names in the global store."""
    _get_thread_local_store()[_DEFAULT_OVERRIDE_KEY] = default_overrides


def get_all_calc_objects() -> list:
    """Get all calculation objects saved in the global store."""
    return _get_thread_local_store()[_ALL_CALC_ITEMS_KEY]


def clear_all_input_default_overrides():
    """Clear all input default overrides from the global store."""
    _get_thread_local_store()[_DEFAULT_OVERRIDE_KEY] = {}


def _get_float_safe_operation(
    input_operation: Operation | Expression | Variable | float | int,
):
    if isinstance(input_operation, (float, int)):
        return Operation("", input_operation)
    else:
        return input_operation
