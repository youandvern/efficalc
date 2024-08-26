from efficalc.report_builder import ReportBuilder
from full_calc_document import calculation

col_data1 = (40, 40, "#7", 1.5, 8, 9, 11000, 80, False, False)

# for each load case: Mx, My, P, and whether the calc should be shown
load_cases1 = [[800, 100, 400, True], [0, 0, -2200, True]]
new_inputs = {"col_data": col_data1, "load_cases": load_cases1}

builder = ReportBuilder(calculation, new_inputs)
builder.view_report()
