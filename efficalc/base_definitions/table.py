from typing import Any, List, Optional

from .shared import (
    CalculationItem,
    get_override_or_default_value,
    save_calculation_item,
)


class Table(CalculationItem):
    """An object to display a table of data.

    :param data: The data in the table. If this is an input table, the data will act as default data to be overridden
        by the calculation runner.
    :type data: List[List[Any]] (a 2d list where each inner list is a row in the table)
    :param headers: The headers for the table, defaults to None
    :type headers: List[Any], optional
    :param title: The table title, defaults to None
    :type title: str, optional
    :param striped: Whether the table should be striped, defaults to False
    :type striped: bool, optional
    :param full_width: Whether the table should be full width, defaults to False
    :type full_width: bool, optional
    :param result_check: This is used to indicate any :class:`.Table` that should be checked as a final result
        of your calculation template. When set to True, this :class:`.Table` will be displayed in the "Results"
        section of your design portal in the cloud version of efficalc, defaults to False
    :type result_check: bool, optional
    :param numbered_rows: Whether to add row numbers (starting at 1) to each row, defaults to False
    :type numbered_rows: bool, optional

    """

    def __init__(
        self,
        data: List[List[Any]],
        headers: Optional[List[any]] = None,
        title: Optional[str] = None,
        striped: bool = False,
        full_width: bool = False,
        result_check: bool = False,
        numbered_rows: bool = False,
    ) -> None:
        self.data = data
        self.headers = headers
        self.title = title
        self.striped = striped
        self.full_width = full_width
        self.result_check = result_check
        self.numbered_rows = numbered_rows
        save_calculation_item(self)

    def __str__(self) -> str:
        return f"{self.title}\n{self.headers}\n{self.data}"


class InputTable(Table):
    """A table that can be used to accept dynamic input data with the calculation runner and cloud version of efficalc.

    :param default_data: The default data for the table. This will be overridden when explicit calculation inputs are
        provided to the calculation runner or in the design portal on the cloud version of efficalc
    :type default_data: List[List[Any]]
    :param headers: The headers for the table. This will be used as the unique identifier for the input table
    :type headers: List[Any]
    :param title: The table title, defaults to None
    :type title: str, optional
    :param striped: Whether the table should be striped, defaults to False
    :type striped: bool, optional
    :param full_width: Whether the table should be full width, defaults to True
    :type full_width: bool, optional
    :param numbered_rows: Whether to add row numbers (starting at 1) to each row, defaults to False
    :type numbered_rows: bool, optional
    """

    def __init__(
        self,
        default_data: List[List[Any]],
        headers: List[any],
        title: Optional[str] = None,
        striped: bool = False,
        full_width: bool = False,
        numbered_rows: bool = False,
    ) -> None:
        super().__init__(
            default_data, headers, title, striped, full_width, False, numbered_rows
        )
        self.data = get_override_or_default_value(self.identifier, default_data)

    @property
    def identifier(self):
        return "input_table-" + "-".join(self.headers)

    def __str__(self) -> str:
        return f"{self.title}\n{self.headers}\n{self.data}"
