from enum import Enum

from latexexpr_efficalc import Variable

from .shared import (
    CalculationItem,
    get_override_or_default_value,
    save_calculation_item,
)


class InputType(Enum):
    NUMBER = "number"
    TEXT = "text"


class Input(Variable, CalculationItem):
    """This is the primary object used to define an input which can change from calculation to calculation. Inputs may
    be numbers, text, or select elements with multiple options.

    :param variable_name: The symbolic name for this input variable (LaTex formatted)
    :type variable_name: str
    :param default_value: The default value for the input which will be overridden when calculation inputs are
        updated, defaults to 0
    :type default_value: float, int, or str
    :param unit: The physical units of the input variable (LaTex formatted), defaults to None
    :type unit: str, optional
    :param description: A text description for the input variable, defaults to None
    :type description: str, optional
    :param reference: A short text reference (or code reference) to accompany the input, defaults to None
    :type reference: str, optional
    :param select_options: A list of options for a select type input variable, defaults to None
    :type select_options: str[], float[], or int[], optional
    :param min_value: Set the minimum value a number input is allowed to be, defaults to None
    :type min_value: float, int, or None, optional
    :param max_value: Set the maximum value a number input is allowed to be, defaults to None
    :type max_value: float, int, or None, optional
    :param num_step: Specifies the interval between legal numbers in a number input field; see
        https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/step, defaults to None
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
        unit: str = "",
        description: str = "",
        reference: str = "",
        select_options: list = None,
        min_value: int | float = None,
        max_value: int | float = None,
        num_step: int | float | str = "any",
    ):
        override_or_default_value = get_override_or_default_value(
            variable_name, default_value
        )

        super().__init__(variable_name, override_or_default_value, unit)
        self.description = description
        self.reference = reference
        self.num_step = num_step
        self.min_value = min_value
        self.max_value = max_value
        self.select_options = select_options
        save_calculation_item(self)

    def str_result_with_name(self):
        # r"""Returns string of the result of the receiver (its formatted result) including name ending with its units
        #
        # :rtype: str
        #
        # .. code-block:: python
        #
        # >>> v1 = Input('a_{22}',3.45,'mm',description="Section thickness")
        # >>> print v1.str_result_with_description()
        #     a_{22} = 3.45 \ \mathrm{mm}
        # """
        return "%s = \\ %s \\ %s" % (
            self.name,
            self.str_result(),
            self.unitFormat % self.unit,
        )

    def get_value(self):
        """Returns the value of the input. This will not always return the default value that is set in the template,
        but will return the updated input value in each unique calculation instance.

        :return: The current value of the input variable
        :rtype: float, int, or str

        .. code-block:: python

            >>> a = Input('a',1,'ft')
            >>> print(a.get_value())
            1
        """
        return self.value

    def __str__(self):
        if self._get_display_type() != InputType.NUMBER:
            return rf"\mathrm{{{self.name}}} = \mathrm{{{self.value}}} \ {self.unit}"
        else:
            return super().__str__()

    def _get_display_type(self) -> InputType:
        try:
            float(self.value)
            return InputType.NUMBER
        except ValueError:
            return InputType.TEXT
