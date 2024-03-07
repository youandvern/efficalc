import os
import tempfile
import webbrowser
from dataclasses import dataclass
from typing import Callable

from efficalc.calculation_runner import CalculationRunner
from efficalc.generate_html import generate_html_for_calc_items


class CalculationReportBuilder(object):
    """
    A helper class to run calculation functions and generate reports based on the calculations.

    This class provides methods to run a calculation function with optional input value overrides and generate an HTML
    report to view or print the calculations. Reports can be viewed immediately in a web browser, saved to a file, or
    returned as a string.

    :param calc_function: The calculation function to be executed. This function should define the calculations to be
        performed and instantiate calculation objects accordingly. It will be executed using the
        :class:`CalculationRunner`.
    :type calc_function: Callable
    :param input_vals: A dictionary of values to override the calculation function's default input values. Keys should
        be the names of the input objects in the calculation function and values should be the desired values for the
        input.
    :type input_vals: dict[str, any], optional
    """

    def __init__(
        self,
        calc_function: Callable,
        input_vals: dict[str, any] = None,
    ):
        self.calc_function: Callable = calc_function
        self.input_default_overrides: dict[str, any] = (
            input_vals if input_vals is not None else {}
        )

    def view_report(self) -> str:
        """Runs the calculation function with the provided input overrides and opens up the calculation report in the
        default web browser. The report is generated as a temporary HTML file which can be printed to PDF or any other
        format.

        :return: The path to the temporary HTML file.
        :rtype: str
        """
        html_content = self.__generate_report_html()

        # Create a temporary HTML file and get its path
        temp_file_path = _create_temp_html_file(html_content)

        # Open the temporary file in the default web browser
        webbrowser.open("file://" + os.path.realpath(temp_file_path))

        return temp_file_path

    def get_html_as_str(self) -> str:
        """Runs the calculation function with the provided input overrides and generates a string that is a complete
        HTML document with the calculation report.

        :return: The HTML report as a string.
        :rtype: str
        """
        return self.__generate_report_html()

    def save_report(
        self,
        folder_path: str,
        file_name: str = "calc_report",
        open_on_create: bool = False,
    ) -> str:
        """Runs the calculation function with the provided input overrides and saves the calculation report at the
        specified location.

        The report is generated as an HTML file with the provided `file_name` and saved at the
        provided `folder_path`. It will also open in the default web browser if `open_on_create` is set to True. If
        the `folder_path` does not exist, it will be created.

        :param folder_path: the path to the folder where the report will be saved
        :type folder_path: str
        :param file_name: the name of the html file that will be created in the `folder_path`, defaults to "calc_report"
        :type file_name: str, optional
        :param open_on_create: if True, the report will be opened in the default web browser, defaults to False
        :type open_on_create: bool
        :return: the complete filepath of the saved html file
        :rtype: str
        """

        # Create the requested folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        full_file_path = os.path.join(folder_path, f"{file_name}.html")

        html_content = self.__generate_report_html()

        with open(full_file_path, "w") as file:
            file.write(html_content)

        if open_on_create:
            # Open the created file in the default web browser
            webbrowser.open("file://" + os.path.realpath(full_file_path))

        return full_file_path

    def __generate_report_html(self):
        calculation = CalculationRunner(
            self.calc_function, self.input_default_overrides
        )

        all_items = calculation.calculate_all_items()
        report_items_html = generate_html_for_calc_items(all_items)

        return _wrap_report_in_html_page(report_items_html)


def _create_temp_html_file(html_content):
    # Create a temporary file to write HTML content
    # Use delete=False to keep the file after closing
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as temp_file:
        temp_file.write(html_content)
        # Return the path of the temporary file
        return temp_file.name


def _wrap_report_in_html_page(content: str) -> str:
    start = """
    <!DOCTYPE html>
    <html style="background-color: #eeeeee;">
    <head>
    <script type="text/javascript" async
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
    <style>
        body {
            box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
            max-width: 850px; 
        }
        p {
            margin-block-start: 0;
            margin-block-end: 0;
            line-height: 1.5;
        }
        .calc-item {
            margin-block: 1.5rem;
        }
        @media print {
            body {
                box-shadow: none;
                max-width: none;
            }
        }
    </style>
    </head>
    <body style="margin-inline: auto; padding: 1rem; background-color: #ffffff;">
    """
    end = """
    </body>
    </html>
    """
    return start + content + end
