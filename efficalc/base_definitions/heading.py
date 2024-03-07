from typing import Literal

from .shared import CalculationItem, save_calculation_item


class Heading(CalculationItem):
    """This object can be used to add headings/section titles to calculation reports. If numbered, the heading number
    will auto-increment. The text size will generally be larger for higher levels (i.e. 1) than lower levels (i.e. 6)

    :param text: The text for the heading or title
    :type text: str
    :param head_level: The level of the heading from 1 to 6. Each heading level in its corresponding position would
        display as 1.2.3.4.5.6. before the heading text, defaults to 1
    :type head_level: int, optional
    :param numbered: Whether the heading should be numbered or not, defaults to True
    :type numbered: bool, optional

    .. code-block:: python

        >>> Heading("Default First Heading", head_level=1)
        >>> Heading("Second Level Heading", head_level=2)
        >>> Heading("Another Second Level Heading", head_level=2)
        >>> Heading("Heading Without Number", head_level=2, numbered=False)
        Calculation report will show -->    1.  Default First Heading
                                            1.1.  Second Level Heading
                                            1.2.  Another Second Level Heading
                                            Heading Without Number
    """

    def __init__(
        self,
        text: str,
        head_level: Literal[1, 2, 3, 4, 5, 6, 7, 8] = 1,
        numbered: bool = True,
    ):
        self.text = text
        self.description = self.text
        self.head_level = head_level  # 1 - 6
        self.numbered = numbered
        save_calculation_item(self)

    def __str__(self):
        return f"{self.text}"
