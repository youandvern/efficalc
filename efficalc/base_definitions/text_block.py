from .shared import CalculationItem, save_calculation_item


class TextBlock(CalculationItem):
    """This displays a block of text in the calculation report.

    :param text: The text
    :type text: str
    :param reference: A short text reference (e.g. code reference) to accompany the text, defaults to None
    :type reference: str, optional
    """

    def __init__(self, text: str, reference: str = None):
        self.text: str = text
        self.description: str = self.text
        self.reference: str = reference
        save_calculation_item(self)

    def __str__(self):
        return f"{self.text}" if self.text else ""
