from examples.conc_col_pmm.calc_document.document_wrapper import run

col_data = [24, 36, "#8", 2, 5, 4, 8000, "60 ksi", "Edge", "Tied"]

# for each load case: P, Mx, My, and whether the calc should be shown
# Note that these load cases currently do not override the defaults
loads = [[300, 100, 200, True], [-100, 50, -60, False], [11500, 300, -300, False]]

run(True, col_data, loads)
