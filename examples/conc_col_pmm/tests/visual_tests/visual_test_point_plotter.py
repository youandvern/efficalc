import matplotlib.pyplot as plt

from efficalc import Input

from ...calc_document.plotting import get_capacity, pmm_mesh, point_plotter
from ...col import assign_max_min
from ...col.column import Column
from ...constants.rebar_data import BarSize
from ...pmm_search.load_combo import LoadCombination
from ...tests.conftest import getCalculatedColumnProps


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
    loads = [LoadCombination(i, *load) for i, load in enumerate(load_data)]

    _, _, _, mesh = pmm_mesh.get_mesh(col, 36, 12, axial_limits)

    capacity = get_capacity.get_capacity(mesh, loads[0])
    fig = point_plotter.plot(capacity, loads[0], False)

    plt.show()

    # plt.savefig("test_plot.png")
