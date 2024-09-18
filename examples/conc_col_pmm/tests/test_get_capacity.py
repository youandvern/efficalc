from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_plotter_plotly,
)


def test_get_capacity(example_col, loads):

    col = example_col
    col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
    # maximum and minimum allowable loads, to be used for normalizing error

    mesh, _ = pmm_plotter_plotly.plot(col, 36, 12, loads)

    _ = get_capacity.get_capacity(mesh, loads[0][:3])
