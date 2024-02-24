from typing import Literal

from latexexpr_efficalc import Expression, Operation, Variable

from .input import Input
from .shared import OPERATOR_TO_LATEX, CalculationItem, save_calculation_item


class ComparisonStatement(CalculationItem):
    """This is an object for declaring the result of a comparison. It does not actually compare the values given, but
    rather displays the comparision exactly as it is given. This can be used to annotate or embellish if/else logic in
    your calculation templates.

    :param a: The first variable or number
    :type a: :class:`.Input`, :class:`.Calculation`, or a number
    :param comparator: The comparision symbol as a string
    :type comparator: '<', '<=', '=', '!=', '==', '>', or '>='
    :param b: The second variable or number
    :type b: :class:`.Input`, :class:`.Calculation`, or a number
    :param comparator2: A second comparision symbol as a string, defaults to None
    :type comparator2: '<', '<=', '=', '!=', '==', '>', or '>=', optional
    :param c: A third variable or number, defaults to None
    :type c: :class:`.Input`, :class:`.Calculation`, or a number, optional
    :param description: A text description for the comparison, defaults to None
    :type description: str, optional
    :param reference: A short text reference (or code reference) to accompany the comparison, defaults to None
    :type reference: str, optional

    .. code-block:: python

        >>> a = Input("a",1,'ft')
        >>> b = Input('b',4,'ft')
        >>> ComparisonStatement(a, ">", b, description="Requirement for passing")
        Calculation report will show --> Requirement for passing:
                                            --> a > b
    """

    def __init__(
        self,
        a: Variable | Operation | Expression | float | int,
        comparator: Literal["<", "<=", "=", "!=", "==", ">", ">="],
        b: Variable | Operation | Expression | float | int,
        comparator2: Literal["<", "<=", "=", "!=", "==", ">", ">="] = None,
        c: Variable | Operation | Expression | float | int = None,
        description: str = "",
        reference: str = "",
    ):
        self.a: Variable | Operation | Expression | float | int = a
        self.comparator: Literal["<", "<=", "=", "!=", "==", ">", ">="] = comparator
        self.b: Variable | Operation | Expression | float | int = b
        self.comparator2: Literal["<", "<=", "=", "!=", "==", ">", ">="] | None = (
            comparator2
        )
        self.c: Variable | Operation | Expression | float | int = c
        self.description: str = description
        self.reference: str = reference
        self.result_check: bool = False
        save_calculation_item(self)

    def str_symbolic(self):

        all_inputs = [self.a, self.b, self.c]
        str_inputs = []

        for item in all_inputs:
            if hasattr(item, "name"):
                str_input = item.name
            elif hasattr(item, "str_symbolic"):
                str_input = item.str_symbolic()
            else:
                str_input = str(item)
            str_inputs.append(str_input)

        if self.comparator2 is not None and self.c is not None:
            return f"{str_inputs[0]} \ {OPERATOR_TO_LATEX[self.comparator]} \ {str_inputs[1]} \ {OPERATOR_TO_LATEX[self.comparator2]}  \ {str_inputs[2]}"
        else:
            return f"{str_inputs[0]} \ {OPERATOR_TO_LATEX[self.comparator]} \ {str_inputs[1]}"

    def __str__(self):
        return self.str_symbolic()
