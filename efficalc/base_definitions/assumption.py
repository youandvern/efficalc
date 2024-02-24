from .shared import CalculationItem, save_calculation_item


class Assumption(CalculationItem):
    """This is meant to clearly declare important assumptions which form the basis of your calculation template.

    :param assumption: The text describing your assumption
    :type assumption: str

    .. code-block:: python

        >>> a = Assumption("The seismic provisions of ASCE 7-16 control design")
        Calculation report will show --> [ASSUME] The seismic provisions of ASCE 7-16 control design
    """

    def __init__(self, assumption: str):
        self.text: str = assumption
        save_calculation_item(self)

    def __str__(self):
        return f"{self.text}"
