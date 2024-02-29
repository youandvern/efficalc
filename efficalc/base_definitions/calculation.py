from enum import Enum

from latexexpr_efficalc import Expression, Operation, Variable
from pylatexenc.latex2text import LatexNodes2Text

from .input import Input
from .shared import CalculationItem, _get_float_safe_operation, save_calculation_item


class CalculationLength(Enum):
    NUMBER = "number"
    SHORT = "short"
    LONG = "long"


class Calculation(Expression, CalculationItem):
    """This is the primary object used to define a calculation expression or calculated variable.

    :param variable_name: The symbolic name for the result of this calculation (LaTex formatted)
    :type variable_name: str
    :param expression: The calculation expression
    :type expression: a variable expression [i.e. a+b] or a number
    :param unit: The physical units of the resulting variable (LaTex formatted), defaults to None
    :type unit: str, optional
    :param description: A text description for the calculation or calculated variable, defaults to None
    :type description: str, optional
    :param reference: A short text reference (or code reference) to accompany the calculation, defaults to None
    :type reference: str, optional
    :param result_check: This is used to indicate any :class:`.Calculation` that should be checked as a final result
        of your calculation template. When set to True, this :class:`.Calculation` will be displayed in the "Results"
        section of your design portal, defaults to False
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
        unit: str = "",
        description: str = "",
        reference: str = "",
        result_check: bool = False,
    ):

        super().__init__(variable_name, _get_float_safe_operation(expression), unit)
        self.description: str = description
        self.reference: str = reference
        self.result_check: bool = result_check
        self.error: str | None = None
        save_calculation_item(self)

    def str_result_with_description(self):
        # r"""Returns string representation of receiver in the form "description; name = symbolicExpr"
        #
        # :rtype: str
        #
        # .. code-block:: python
        #
        #     >>> v1 = Variable('a_{22}',3.45,'mm')
        #     >>> v2 = Variable('F',5.876934835,'kN')
        #     >>> v3 = Variable('F',4.34,'kN',exponent=-2)
        #     >>> e2 = Calculation('E_2',(v1+v2)/v3,'mm', description="Section thickness")
        #     >>> print e2.str_result_with_description()
        #     Section thickness; E_2 = \frac{ {a_{22}} + {F} }{ {F} }
        # """
        if self.is_symbolic():
            return f"{self.name} = {self.operation}"
        return f"{self.description}; {self.name} = {self.operation.str_symbolic()}"

    def str_substituted(self):
        return self.operation.str_substituted()

    def str_symbolic(self):
        return self.operation.str_symbolic()

    def result(self):
        """See `get_value`"""
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
        """Returns the calculated value of the expression.

        :return: The result of the evaluated expression
        :rtype: float or int

        .. code-block:: python

            >>> a = Input('a',1,'ft')
            >>> b = Input('b',4,'ft')
            >>> c = Calculation('c', a + b, 'ft')
            >>> print(c.get_value())
            5
        """
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
        if (
            self._get_symbolic_string().strip()
            == self._get_substituted_string().strip()
        ):
            return CalculationLength.NUMBER
        elif self._estimate_operation_length() <= 50:
            return CalculationLength.SHORT
        else:
            return CalculationLength.LONG
