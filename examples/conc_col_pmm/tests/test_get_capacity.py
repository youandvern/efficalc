from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_plotter_plotly,
)
from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits


def test_get_capacity(example_col, loads):

    col = example_col
    axial_limits = calculate_axial_load_limits(col)

    mesh, _ = pmm_plotter_plotly.plot(col, 36, 12, loads, axial_limits)

    _ = get_capacity.get_capacity(mesh, loads[0])
