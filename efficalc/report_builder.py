import os
import tempfile
import webbrowser
from dataclasses import dataclass
from typing import Callable

from efficalc.calculation_runner import CalculationRunner
from efficalc.generate_html import generate_html_for_calc_items


# TODO: option to return html string, save html file somewhere, or just show it
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

    def generate_report(self):
        calculation = CalculationRunner(
            self._calc_function, self._input_default_overrides
        )

        all_items = calculation.calculate_all_items()
        report_items_html = generate_html_for_calc_items(all_items)

        html_content = wrap_report(report_items_html)

        # Create a temporary HTML file and get its path
        temp_file_path = create_temp_html_file(html_content)

        # Open the temporary file in the default web browser
        webbrowser.open("file://" + os.path.realpath(temp_file_path))


def create_temp_html_file(html_content):
    # Create a temporary file to write HTML content
    # Use delete=False to keep the file after closing
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as temp_file:
        temp_file.write(html_content)
        # Return the path of the temporary file
        return temp_file.name


def wrap_report(content: str) -> str:
    start = """
    <!DOCTYPE html>
    <html>
    <head>
    <script type="text/javascript" async
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
    </head>
    <body style="max-width:850px;">
    """
    end = """
    </body>
    </html>
    """
    return start + content + end
