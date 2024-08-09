import os
import tempfile
import webbrowser
from enum import Enum
from typing import Callable

from efficalc.calculation_runner import CalculationRunner
from efficalc.generate_html import generate_html_for_calc_items


class LongCalcDisplayType(Enum):
    """An enumeration for controlling how to display long mathematical expressions in reports.

    :cvar SCALE: Scale the expression display and font size down to fit within the report width
    :cvar LINEBREAK: Break the expression into multiple lines to fit within the report width
    """

    SCALE = "scale"
    LINEBREAK = "linebreak"


class ReportBuilder(object):
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
    :param long_calc_display: How long expressions should be altered to fit within the calculation report width.
        This can be either SCALE for scaling down the display size of the expression or LINEBREAK to break the
        expression into multiple lines. defaults to SCALE
    :type long_calc_display: LongCalcDisplayType, optional
    """

    def __init__(
        self,
        calc_function: Callable,
        input_vals: dict[str, any] = None,
        long_calc_display: LongCalcDisplayType = LongCalcDisplayType.SCALE,
    ):
        self.calc_function = calc_function
        self.input_default_overrides = input_vals if input_vals is not None else {}
        self.long_calc_display = long_calc_display

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
        save_folder: str,
        filename: str = "calc_report",
        open_on_save: bool = False,
    ) -> str:
        """Runs the calculation function with the provided input overrides and saves the calculation report at the
        specified location.

        The report is generated as an HTML file with the provided `file_name` and saved at the
        provided `folder_path`. It will also open in the default web browser if `open_on_create` is set to True. If
        the `folder_path` does not exist, it will be created.

        :param save_folder: the path to the folder where the report will be saved
        :type save_folder: str
        :param filename: the name of the html file that will be created in the `folder_path`, defaults to "calc_report"
        :type filename: str, optional
        :param open_on_save: if True, the report will be opened in the default web browser, defaults to False
        :type open_on_save: bool

        :return: the complete filepath of the saved html file
        :rtype: str
        """

        _create_folder_if_not_exists(save_folder)

        full_file_path = os.path.join(save_folder, f"{filename}.html")

        html_content = self.__generate_report_html()

        with open(full_file_path, "w") as file:
            file.write(html_content)

        if open_on_save:
            # Open the created file in the default web browser
            webbrowser.open("file://" + os.path.realpath(full_file_path))

        return full_file_path

    def __generate_report_html(self):
        calculation = CalculationRunner(
            self.calc_function, self.input_default_overrides
        )

        all_items = calculation.calculate_all_items()
        report_items_html = generate_html_for_calc_items(all_items)

        return _wrap_report_in_html_page(report_items_html, self.long_calc_display)


def _create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def _create_temp_html_file(html_content):
    # Create a temporary file to write HTML content
    # Use delete=False to keep the file after closing
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as temp_file:
        temp_file.write(html_content)
        # Return the path of the temporary file
        return temp_file.name


def _wrap_report_in_html_page(
    content: str, long_calc_display: LongCalcDisplayType
) -> str:

    start = f"""
    <!DOCTYPE html>
    <html style="background-color: #eeeeee;">
    <head>
    <script>
        window.MathJax = {{
            output: {{
                displayOverflow: "{long_calc_display.value}",
            }},
        }};
    </script>
    <script type="text/javascript" async
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/4.0.0-beta.7/tex-mml-chtml.min.js"></script>
    <style>
        body {{
            box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
            max-width: 850px; 
        }}
        p {{
            margin-block-start: 0;
            margin-block-end: 0.5em;
            line-height: 1.1;
        }}
        .calc-item {{
            margin-block: 1.5rem;
        }}
        table {{
          border-collapse: collapse;
        }}
        td, th {{
          border: 1px solid #bdbdbd;
          text-align: left;
          padding: 8px;
        }}
        th {{
          border-bottom: 2px solid #424242;
        }}
        table.striped tr:nth-child(even) {{
          background-color: #e0e0e0;
        }}
        @media print {{
            body {{
                box-shadow: none;
                max-width: none;
            }}
        }}
    </style>
    </head>
    <body style="margin-inline: auto; padding: 1rem; background-color: #ffffff;">
    """
    end = """
    </body>
    </html>
    """
    return start + content + end
