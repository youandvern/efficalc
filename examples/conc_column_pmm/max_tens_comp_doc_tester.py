from efficalc.report_builder import ReportBuilder
from max_tens_comp import calculation
import sections


def nested_calculation():
    col = sections.Column(20, 30, "#8", 1.5, 3, 5, 8000, 60, False, False)


builder = ReportBuilder(nested_calculation)
builder.view_report()
