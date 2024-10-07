import matplotlib.pyplot as plt

from efficalc import Input
from examples.conc_col_pmm.calc_document.plotting import (
    get_capacity,
    pmm_plotter_plotly,
    point_plotter,
)
from examples.conc_col_pmm.col import assign_max_min
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.constants.rebar_data import BarSize
from examples.conc_col_pmm.pmm_search.load_combo import LoadCombination
from examples.conc_col_pmm.tests.conftest import getCalculatedColumnProps


def example_col():
    bar_size: BarSize = "#5"
    calc_props = getCalculatedColumnProps(bar_size)

    return Column(
        Input("w", 24),
        Input("h", 18),
        Input("bar_size", bar_size),
        Input("cover", 1.5),
        Input("nx", 5),
        Input("ny", 4),
        Input("f'_c", 8000),
        Input("f_y", 80),
        False,
        False,
        calc_props["A_b"],
        calc_props["E_s"],
        calc_props["e_c"],
    )


if __name__ == "__main__":
    col = example_col()
    axial_limits = assign_max_min.calculate_axial_load_limits(col)

    # for each load case: P, Mx, My, and whether the calc should be shown
    load_data = [
        [300, 100, 200, True],
        [-100, 50, -60, False],
        [11500, 300, -300, False],
    ]
    loads = [LoadCombination(*load) for load in load_data]

    mesh, _ = pmm_plotter_plotly.plot(col, 36, 12, loads, axial_limits)

    capacity = get_capacity.get_capacity(mesh, loads[0])
    fig = point_plotter.plot(capacity, loads[0], False)

    # fig.show()
    plt.show()

    # plt.savefig("test_plot.png")
