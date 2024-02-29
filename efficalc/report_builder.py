import os
import tempfile
import webbrowser
from dataclasses import dataclass
from typing import Callable

from efficalc.calculation_runner import CalculationRunner
from efficalc.generate_html import generate_html_for_calc_items


@dataclass
class CalculationReportConfig(object):
    save_path: str = None  # defaults to working directory
    file_name: str = None  # defaults to <calc_function_name>_report.pdf
    display_on_generate: bool = True
    title_override: str = None  # will only override the first title in the document


class CalculationReportBuilder(object):

    def __init__(
        self,
        calc_function: Callable,
        input_vals: dict[str, any] = None,
        config: CalculationReportConfig = None,
    ):
        self._calc_function: Callable = calc_function
        self._input_default_overrides: dict[str, any] = (
            input_vals if input_vals is not None else {}
        )
        self._config: CalculationReportConfig = (
            config if config is not None else CalculationReportConfig()
        )

    def set_calc_function(self, calc_function: Callable):
        self._calc_function = calc_function

    def set_config(self, config: CalculationReportConfig):
        self._config = config

    def set_input_vals(self, input_vals: dict[str, any] = None):
        self._input_default_overrides = input_vals

    def view_report(self):
        html_content = self.__generate_report_html()

        # Create a temporary HTML file and get its path
        temp_file_path = _create_temp_html_file(html_content)

        # Open the temporary file in the default web browser
        webbrowser.open("file://" + os.path.realpath(temp_file_path))

    def get_html_as_str(self):
        return self.__generate_report_html()

    def save_report(
        self,
        folder_path: str,
        file_name: str = "calc_report",
        open_on_create: bool = False,
    ) -> None:

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

    def __generate_report_html(self):
        calculation = CalculationRunner(
            self._calc_function, self._input_default_overrides
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
