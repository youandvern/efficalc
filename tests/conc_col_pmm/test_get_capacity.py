from examples.conc_col_pmm.calc_document.plotting import get_capacity, pmm_plotter


def test_get_capacity(example_col):

    col = example_col
    col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
    # maximum and minimum allowable loads, to be used for normalizing error

    mesh, _ = pmm_plotter.plot(col, 36, 12)

    # define a load with Mx, My, and then P, all ultimate
    load = [200, -100, 400]

    capacity_pts = get_capacity.get_capacity(mesh, load)
