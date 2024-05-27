from latexexpr_efficalc import Expression, Operation, Variable
from pylatexenc.latex2text import LatexNodes2Text

from .. import CalculationLength
from .input import Input
from .shared import (
    CalculationItem,
    _get_float_or_str_safe_operation,
    save_calculation_item,
)


class Symbolic(Expression, CalculationItem):
    """This will disply a symbolic variable expression in the calculation report. A substituted expression with values
    will not be displayed, nor will the result of the expression. You can optionally evaluate the result to use as a
    number in pure python calculations.

    :param variable_name: The symbolic name for the result of this calculation (LaTex formatted)
    :type variable_name: str
    :param expression: The calculation expression
    :type expression: a variable expression [i.e. a+b] or a constant number
    :param description: A text description for the calculation, defaults to None
    :type description: str, optional
    :param reference: A short reference (e.g. code reference) to accompany the calculation, defaults to None
    :type reference: str, optional
    :param result_check: This is used to indicate any :class:`.Symbolic` that should be listed with the final results
        of your calculation template. When set to True, this :class:`.Symbolic` will be displayed in the "Results"
        section of your design portal in the cloud version of efficalc, defaults to False
    :type result_check: bool, optional

    .. code-block:: python

        >>> a = Input("a",1,'ft')
        >>> b = Input('b',4,'ft')
        >>> c = Symbolic('c', a + b)
        Calculation report will show --> c = a + b
    """

    def __init__(
        self,
        variable_name: str,
        expression: Operation | Expression | Variable | float | int | str,
        description: str = None,
        reference: str = None,
        result_check: bool = False,
    ):

        super().__init__(
            variable_name, _get_float_or_str_safe_operation(expression), ""
        )
        self.description: str = description
        self.reference: str = reference
        self.result_check: bool = result_check
        self.error: str | None = None
        save_calculation_item(self)

    def str_result_with_description(self) -> str:
        """Returns a LaTex formatted string representation of the operation in the form "description; name = symbolicExpr" """
        if self.is_symbolic():
            return f"{self.description}; {self.name} = {self.operation}"
        return f"{self.description}; {self.name} = {self.operation.str_symbolic()}"

    def str_substituted(self) -> str:
        """Alias for :func:`.Symbolic.str_symbolic`"""
        return self.str_symbolic()

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
            >>> c = Symbolic('c', a + b, 'ft')
            >>> print(c.result())
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
        """Alias for :func:`.Symbolic.result`"""
        return self.result()

    def _estimate_operation_length(self):
        latex_code = self.operation.str_symbolic()
        return len(LatexNodes2Text().latex_to_text(latex_code))

    def _get_symbolic_string(self):
        latex_code = self.operation.str_symbolic()
        return LatexNodes2Text().latex_to_text(latex_code)

    def estimate_display_length(self) -> CalculationLength:
        """Returns the estimated length of the LaTex formatted operation based on its symbolic
        representation.

        :return: The estimated length of the :class:`.Symbolic`
        :rtype: :class:`.CalculationLength`

        .. code-block:: python

            >>> a = Input('a',2,'ft')
            >>> b = Input('b',3,'ft')
            >>> c = Symbolic('c', a + b, 'ft')
            >>> c.estimate_display_length()
            CalculationLength.SHORT
        """
        if self._estimate_operation_length() <= 50:
            return CalculationLength.SHORT
        else:
            return CalculationLength.LONG

    def str_result_with_unit(self):
        """Alias for :func:`.Symbolic.__str__`"""
        return str(self)

    def __str__(self):
        return f"{self.name} = {self.str_symbolic()}"
