from examples.conc_col_pmm.calc_document.plotting import pmm_plotter_plotly


# This test checks for runtime errors
def test_pmm_plotter_plotly(example_col, loads):

    col = example_col
    col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
    # maximum and minimum allowable loads, to be used for normalizing error

    load_cases = loads[:3]

    _, _ = pmm_plotter_plotly.plot(col, 36, 12, load_cases)
