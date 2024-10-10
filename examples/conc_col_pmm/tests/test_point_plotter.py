from ..calc_document.plotting import get_capacity, pmm_mesh, point_plotter
from ..col.assign_max_min import calculate_axial_load_limits

# This test checks for runtime errors


def test_point_plotter(example_col3, loads):

    axial_limits = calculate_axial_load_limits(example_col3)
    _, _, _, mesh = pmm_mesh.get_mesh(example_col3, 36, 12, axial_limits)

    capacity = get_capacity.get_capacity(mesh, loads[0])
    _ = point_plotter.plot(capacity, loads[0], False)
