from examples.conc_col_pmm.calc_document.plotting import pmm_plotter_plotly
from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits


# This test checks for runtime errors
def test_pmm_plotter_plotly(example_col, loads):

    col = example_col
    axial_limits = calculate_axial_load_limits(col)

    load_cases = loads[:3]

    _, _ = pmm_plotter_plotly.plot(col, 36, 12, load_cases, axial_limits)
