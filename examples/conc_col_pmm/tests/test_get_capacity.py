from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_mesh
)
from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits

def test_get_capacity(example_col, loads):

    col = example_col
    axial_limits = calculate_axial_load_limits(col)

    # Retrieve the quarter PMM mesh, which has points
    # in the format (Mx, My, P).
    _, _, _, mesh = pmm_mesh.get_mesh(col, 48, 18, axial_limits)

    _ = get_capacity.get_capacity(mesh, loads[0])
