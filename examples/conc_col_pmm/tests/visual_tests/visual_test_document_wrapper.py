import os
import sys

# Now you can import from conc_col_pmm
from examples.conc_col_pmm.calc_document.document_wrapper import run

# "w", "h", "bar_size", "bar_cover", "bars_x", "bars_y", "fc", "fy", "cover_type", "transverse_type",
col_data = [18, 24, "#6", 2, 5, 2, 8000, 60, "Edge", "Tied"]

# for each load case: P, Mx, My, and whether the calc should be shown
# Note that these load cases currently do not override the defaults
loads = [
    [500, 200, 100, "yes"],
    [-100, 50, -60, "no"],
    [11500, 300, -300, "no"],
]

# calc_report_example1
# col_data = [24, 18, "#6", 1.5, 5, 4, 8000, 60, "Edge", "Tied"]
# loads = [[1400, -300, 100, True]]

# calc_report_example2
# col_data = [24, 36, "#8", 2, 6, 8, 8000, 60, "Edge", "Tied"]
# loads = [[3000, -200, 100, True]]

if __name__ == "__main__":
    run(True, col_data, loads)
