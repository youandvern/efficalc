from ..calc_document.plotting import get_pmm_data, pmm_plotter_plotly
from ..col import assign_max_min
from ..pmm_search.load_combo import LoadCombination


# This test checks for runtime errors
def test_pmm_plotter_plotly(example_col, loads):
    axial_limits = assign_max_min.calculate_axial_load_limits(example_col)

    # for each load case: P, Mx, My, and whether the calc should be shown
    load_data = [
        [300, 100, 200, True],
        [-100, 50, -60, False],
        [1500, 300, -300, False],
    ]
    loads = [LoadCombination(i, *load) for i, load in enumerate(load_data)]

    pmm_data = get_pmm_data.get_pmm_data(example_col, 36, 12, loads, axial_limits)

    _ = pmm_plotter_plotly.plot(pmm_data)
