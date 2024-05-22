from typing import Literal

from latexexpr_efficalc import Expression, Operation, Variable

from .input import Input
from .shared import OPERATOR_TO_LATEX, CalculationItem, save_calculation_item


class Comparison(CalculationItem):
    """This is an object used to compare variables or constants as an explicit check in the calculations. It will
    compare the value of `self.a` against the value of `self.b` using the specified comparator and didplay a message
    depending on whether the comparison is true or false.

    :param a: The first variable or number
    :type a: :class:`.Input`, :class:`.Calculation`, or a number
    :param comparator: The comparision symbol as a string
    :type comparator: '<', '<=', '=', '!=', '==', '>', or '>='
    :param b: The second variable or number
    :type b: :class:`.Input`, :class:`.Calculation`, or a number
    :param true_message: The message that should desplay if the :class:`.Comparison` result is true, defaults to "OK"
    :type true_message: str, optional
    :param false_message: The message that should desplay if the :class:`.Comparison` result is false, defaults to
        "ERROR"
    :type false_message: str, optional
    :param description: A text description for the comparison, defaults to None
    :type description: str, optional
    :param reference: A short text reference (e.g. code reference) to accompany the comparison, defaults to None
    :type reference: str, optional
    :param result_check: This is used to indicate any :class:`.Comparison` that should be checked as a final result
        of your calculation template. When set to True, this :class:`.Comparison` will be displayed in the "Results"
        section of your design portal in the cloud version of efficalc, defaults to False
    :type result_check: bool, optional

    .. code-block:: python

        >>> a = Input("a",1,'ft')
        >>> b = Input('b',4,'ft')
        >>> Comparison(a, '>', b)
        Calculation report will show --> Check a > b
                                            1 ft > 4 ft
                                            --> ERROR
    """

    def __init__(
        self,
        a: Variable | Operation | Expression | float | int,
        comparator: Literal["<", "<=", "=", "!=", "==", ">", ">="],
        b: Variable | Operation | Expression | float | int,
        true_message: str = "OK",
        false_message: str = "ERROR",
        description: str = None,
        reference: str = None,
        result_check: bool = True,
    ):

        self.a: Variable | Operation | Expression | float | int = a
        self.comparator: Literal["<", "<=", "=", "!=", "==", ">", ">="] = comparator
        self.b: Variable | Operation | Expression | float | int = b
        self.true_message: str = true_message
        self.false_message: str = false_message
        self.description: str = description
        self.reference: str = reference
        self.result_check: bool = result_check
        self.name: str = self.str_symbolic()
        self._error = None
        save_calculation_item(self)

    def get_value(self) -> bool:
        """Alias for :func:`.is_passing`"""

        return self.is_passing()

    def is_passing(self) -> bool:
        """Returns the calculated value of the comparison (True or False).

        :return: The result of the evaluated comparison
        :rtype: bool

        .. code-block:: python

            >>> a = Input('a',1,'ft')
            >>> b = Input('b',4,'ft')
            >>> c = Comparison(a, ">", b)
            >>> print(c.is_passing())
            False
        """

        OPERATORS = {
            "<": "lt",
            "<=": "le",
            "=": "eq",
            "!=": "ne",
            "==": "eq",
            ">": "gt",
            ">=": "ge",
        }
        if self.comparator not in OPERATORS:
            self._error = f"Comparison operator {self.comparator} is not supported."
            return False

        try:
            value_a = float(self.a)
            value_b = float(self.b)
            method = f"__{OPERATORS[self.comparator]}__"
            result = getattr(value_a, method)(value_b)
            if result is True:
                self._error = None
                return True
            elif result is False:
                self._error = None
                return False
            elif result is NotImplemented:
                self._error = f"The comparison method {self.comparator} is not implemented for {type(self.a).__name__} and {type(self.b).__name__}"
                return False

        except (TypeError, ValueError):
            self._error = f"Unable to compare {self.a} and {self.b} with operator {self.comparator}"
            return False

    def result(self) -> bool:
        """Alias for :func:`.is_passing`"""
        return self.is_passing()

    def get_message(self) -> str:
        """Returns the appropriate message for the result of the comparison (`.true_message` or `.false_message`). If
        there was an error in the comparison, this will return the error message.

        :return: The message for the evaluated comparison reult
        :rtype: str

        .. code-block:: python

            >>> a = Input('a',1,'ft')
            >>> b = Input('b',4,'ft')
            >>> c = Comparison(a, ">", b, false_message="NO GOOD")
            >>> print(c.get_message())
            NO GOOD
        """
        comparison_is_true = self.is_passing()

        if self._error is not None:
            return self._error

        if comparison_is_true:
            return self.true_message
        else:
            return self.false_message

    def str_symbolic(self) -> str:
        """Returns LaTex formatted representation of the comparison using variable names."""

        left = self.a
        right = self.b

        symbolic_types = (Variable, Expression)
        comparison_symbol = OPERATOR_TO_LATEX[self.comparator]

        if isinstance(left, symbolic_types) and isinstance(right, symbolic_types):
            return rf"\ {left.name} \ & {comparison_symbol} \ {right.name}"
        elif isinstance(left, symbolic_types):
            return rf"\ {left.name} \ & {comparison_symbol} \ {right}"
        elif isinstance(right, symbolic_types):
            return rf"\ {left} \ & {comparison_symbol} \ {right.name}"
        else:
            return self.str_substituted()

    def str_substituted(self) -> str:
        """Returns LaTex formatted representation of the comparison with values substituted in for variables."""

        left = self.a
        right = self.b

        symbolic_types = (Variable, Expression)
        comparison_symbol = OPERATOR_TO_LATEX[self.comparator]

        if isinstance(left, symbolic_types) and isinstance(right, symbolic_types):
            return rf"\ {left.str_result_with_unit()} \ & {comparison_symbol} \ {right.str_result_with_unit()}"
        elif isinstance(left, symbolic_types):
            return rf"\ {left.str_result_with_unit()} \ & {comparison_symbol} \ {right}"
        elif isinstance(right, symbolic_types):
            return rf"\ {left} \ & {comparison_symbol} \ {right.str_result_with_unit()}"
        else:
            return rf"\ {left} \ & {comparison_symbol} \ {right}"

    def __str__(self) -> str:
        return f"Check {self.str_symbolic()} \\rightarrow {self.str_substituted()} \\therefore {self.get_message()}"
