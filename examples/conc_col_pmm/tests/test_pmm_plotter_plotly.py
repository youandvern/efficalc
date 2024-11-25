from ..calc_document.calculation import calculation
from ..calc_document.plotting import get_pmm_data, pmm_plotter_plotly
from ..col import assign_max_min


# This test checks for runtime errors
def test_pmm_plotter_plotly(example_col):
    # for each load case: P, Mx, My, and whether the calc should be shown
    loads = [
        [300, 100, 200, "yes"],
        [-100, 50, -60, "no"],
        [1500, 300, -300, "no"],
    ]

    pmm_data = calculation(default_loads=loads, col=example_col)

    _ = pmm_plotter_plotly.plot(pmm_data)
