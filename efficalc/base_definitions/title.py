from .shared import CalculationItem, save_calculation_item


class Title(CalculationItem):
    """This can be used for the main title in the calculation report. It is larger and bolder than the
    :class:`.Heading` and does not have the option to be numbered.

    :param title: The title
    :type title: str
    """

    def __init__(self, title: str):
        self.text: str = title
        save_calculation_item(self)

    def __str__(self):
        return f"{self.text}"
