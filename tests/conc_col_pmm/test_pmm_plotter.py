from examples.conc_col_pmm.calc_document.plotting import pmm_plotter
import matplotlib.pyplot as plt


def test_pmm_plotter(example_col):

    col = example_col
    col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
    # maximum and minimum allowable loads, to be used for normalizing error

    _, fig = pmm_plotter.plot(col, 36, 12)
    fig.show()
