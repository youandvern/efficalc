from enum import Enum

from latexexpr_efficalc import Expression, Operation, Variable
from pylatexenc.latex2text import LatexNodes2Text

from .input import Input
from .shared import CalculationItem, _get_float_safe_operation, save_calculation_item


class CalculationLength(Enum):
    """Used to indicate the length of a calculation's LaTex formatted operation."""

    NUMBER = "number"
    SHORT = "short"
    LONG = "long"


class Calculation(Expression, CalculationItem):
    """This is the primary object used to define a calculation expression or calculated variable.

    :param variable_name: The symbolic name for the result of this calculation (LaTex formatted)
    :type variable_name: str
    :param expression: The calculation expression
    :type expression: a variable expression [i.e. a+b] or a constant number
    :param unit: The physical units of the resulting variable (LaTex formatted), defaults to None
    :type unit: str, optional
    :param description: A text description for the calculation, defaults to None
    :type description: str, optional
    :param reference: A short reference (e.g. code reference) to accompany the calculation, defaults to None
    :type reference: str, optional
    :param result_check: This is used to indicate any :class:`.Calculation` that should be checked as a final result
        of your calculation template. When set to True, this :class:`.Calculation` will be displayed in the "Results"
        section of your design portal in the hosted version of efficalc, defaults to False
    :type result_check: bool, optional

    .. code-block:: python

        >>> a = Input("a",1,'ft')
        >>> b = Input('b',4,'ft')
        >>> c = Calculation('c', a + b, 'ft')
        Calculation report will show --> c = a + b = 1ft + 4ft = 5ft
    """

    def __init__(
        self,
        variable_name: str,
        expression: Operation | Expression | Variable | float | int,
        unit: str = None,
        description: str = None,
        reference: str = None,
        result_check: bool = False,
    ):

        if unit is None:
            unit = ""
        super().__init__(variable_name, _get_float_safe_operation(expression), unit)
        self.description: str = description
        self.reference: str = reference
        self.result_check: bool = result_check
        self.error: str | None = None
        save_calculation_item(self)

    def str_result_with_description(self) -> str:
        """Returns a LaTex formatted string representation of the operation in the form "description; name = symbolicExpr" """
        if self.is_symbolic():
            return f"{self.name} = {self.operation}"
        return f"{self.description}; {self.name} = {self.operation.str_symbolic()}"

    def str_substituted(self) -> str:
        """Returns LaTex formatted representation of the operation with values substituted in for variables."""
        if self.is_symbolic():
            return self.operation.str_symbolic()
        return self.operation.str_substituted()

    def str_symbolic(self) -> str:
        """Returns LaTex formatted symbolic representation of the operation using the variable names."""
        return self.operation.str_symbolic()

    def result(self) -> float:
        """Returns the calculated result of the expression. If there is a ValueError or ZeroDivisionError, this will
        return 0 and set an error message in `self.error`.

        :return: The result of the evaluated expression
        :rtype: float

        .. code-block:: python

            >>> a = Input('a',2,'ft')
            >>> b = Input('b',3,'ft')
            >>> c = Calculation('c', a + b, 'ft')
            >>> print(c.get_value())
            5
        """
        try:
            return super().result()
        except ValueError:
            self.error = (
                rf"Variable \( {self.name} \) could not be calculated. There has been a math domain error. "
                "Please review and change input variables to an acceptable domain."
            )
            return 0.0
        except ZeroDivisionError:
            self.error = (
                rf"Variable \( {self.name} \) could not be calculated because zero was in the denominator. "
                "Please review and change input variables to an acceptable domain."
            )
            return 0.0

    def get_value(self):
        """Alias for :func:`.Calculation.result`"""
        return self.result()

    def _estimate_operation_length(self):
        latex_code = self.operation.str_substituted()
        self.str_substituted()
        return len(LatexNodes2Text().latex_to_text(latex_code))

    def _get_substituted_string(self):
        latex_code = self.operation.str_substituted()
        return LatexNodes2Text().latex_to_text(latex_code)

    def _get_symbolic_string(self):
        latex_code = self.operation.str_symbolic()
        return LatexNodes2Text().latex_to_text(latex_code)

    def estimate_display_length(self) -> CalculationLength:
        """Returns the estimated length of the LaTex formatted operation based on its symbolic and substituted
        representations.

        :return: The estimated length of the :class:`.Calculation`
        :rtype: :class:`.CalculationLength`

        .. code-block:: python

            >>> a = Input('a',2,'ft')
            >>> b = Input('b',3,'ft')
            >>> c = Calculation('c', a + b, 'ft')
            >>> c.estimate_display_length()
            CalculationLength.SHORT
        """
        if (
            self._get_symbolic_string().strip()
            == self._get_substituted_string().strip()
        ):
            return CalculationLength.NUMBER
        elif self._estimate_operation_length() <= 50:
            return CalculationLength.SHORT
        else:
            return CalculationLength.LONG
