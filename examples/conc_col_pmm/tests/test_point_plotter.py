from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_plotter_plotly,
    point_plotter,
)

# This test checks for runtime errors


def test_point_plotter(example_col3, loads):

    mesh, _ = pmm_plotter_plotly.plot(example_col3, 36, 12, loads)

    # define a load with Mx, My, and then P, all ultimate
    load = [loads[0][1], loads[0][2], loads[0][0]]

    capacity = get_capacity.get_capacity(mesh, load)
    _ = point_plotter.plot(capacity, load, False)
