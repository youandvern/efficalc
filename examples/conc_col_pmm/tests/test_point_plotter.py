from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_plotter_plotly,
    point_plotter,
)
from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits

# This test checks for runtime errors


def test_point_plotter(example_col3, loads):

    axial_limits = calculate_axial_load_limits(example_col3)
    mesh, _ = pmm_plotter_plotly.plot(example_col3, 36, 12, loads, axial_limits)

    capacity = get_capacity.get_capacity(mesh, loads[0])
    _ = point_plotter.plot(capacity, loads[0], False)
