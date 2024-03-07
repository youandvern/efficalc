from enum import Enum
from typing import Literal

from latexexpr_efficalc import Variable

from .shared import (
    CalculationItem,
    get_override_or_default_value,
    save_calculation_item,
)


class InputDisplayType(Enum):
    """Used to indicate whether the input should be displayed as a number or text."""

    NUMBER = "number"
    TEXT = "text"


class Input(Variable, CalculationItem):
    """This is the primary object used to define an input which can change from calculation to calculation. Inputs may
    be numbers, text, or select elements with multiple options.

    :param variable_name: The symbolic name for this input variable (LaTex formatted)
    :type variable_name: str
    :param default_value: The default value for the input. This will be overridden when explicit calculation inputs are
        provided to the calculation runner or in the design portal on the hosted version of efficalc, defaults to 0
    :type default_value: float, int, or str
    :param unit: The physical units of the input variable (LaTex formatted), defaults to None
    :type unit: str, optional
    :param description: A text description for the input variable, defaults to None
    :type description: str, optional
    :param reference: A short text reference (e.g. code reference) to accompany the input, defaults to None
    :type reference: str, optional
    :param input_type: The type of html input element to use in the design portal on the hosted version of efficalc,
        defaults to "number".
    :type input_type: "number", "text", or "select", optional
    :param select_options: A list of options for a "select" input_type variable. This is only applicable when
        `.input_type` is "select", defaults to None
    :type select_options: str[], float[], or int[], optional
    :param min_value: Set the minimum value a number input is allowed to be in the design portal on the hosted version
        of efficalc, defaults to None
    :type min_value: float, int, or None, optional
    :param max_value: Set the maximum value a number input is allowed to be in the design portal on the hosted version
        of efficalc, or "any" if the input type is not a number in the design portal on the hosted version of efficalc, defaults to None
    :type max_value: float, int, or None, optional
    :param num_step: Specifies the interval between legal numbers in a number input field in the design portal on the
        hosted version of efficalc; see
        https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/step, defaults to "any"
    :type num_step: float, int, or None, optional

    .. code-block:: python

        >>> a = Input("a",1,'ft')
        >>> b = Input("b",4,'ft')
        >>> Calculation('c', a + b, 'ft')
        Calculation report will show --> c = a + b = 1ft + 4ft = 5ft
    """

    def __init__(
        self,
        variable_name: str,
        default_value: int | float | str = 0,
        unit: str = None,
        description: str = None,
        reference: str = None,
        input_type: Literal["number", "text", "select"] = "number",
        select_options: list = None,
        min_value: int | float = None,
        max_value: int | float = None,
        num_step: int | float | str = "any",
    ):
        override_or_default_value = get_override_or_default_value(
            variable_name, default_value
        )

        if unit is None:
            unit = ""

        super().__init__(variable_name, override_or_default_value, unit)
        self.description = description
        self.reference = reference
        self.num_step = num_step
        self.min_value = min_value
        self.max_value = max_value
        self.input_type = input_type
        self.select_options = select_options
        save_calculation_item(self)

    def str_result_with_name(self):
        """Returns a LaTex formatted string representation of the input name and value in the form "name = value unit" """
        return "%s = \\ %s \\ %s" % (
            self.name,
            self.str_result(),
            self.unit_format % self.unit,
        )

    def get_value(self):
        """Returns the value of the input. Note that this will return the overridden input value when one is provided
        to the calculation runner or in the design portal on the hosted version of efficalc. If no override is provided,
        this will return the default value.

        :return: The current value of the input variable
        :rtype: float, int, or str

        .. code-block:: python

            >>> a = Input('a',1,'ft')
            >>> print(a.get_value())
            1
        """
        return self.value

    def _get_display_type(self) -> InputDisplayType:
        try:
            float(self.value)
            return InputDisplayType.NUMBER
        except ValueError:
            return InputDisplayType.TEXT

    def __str__(self):
        if self._get_display_type() != InputDisplayType.NUMBER:
            return rf"\mathrm{{{self.name}}} = \mathrm{{{self.value}}} \ {self.unit}"
        else:
            return super().__str__()
