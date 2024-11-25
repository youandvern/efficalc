from efficalc import Input

from ...calc_document.calculation import calculation
from ...calc_document.plotting import pmm_plotter_plotly
from ...col.column import Column
from ...constants.rebar_data import BarSize
from ...tests.conftest import getCalculatedColumnProps

# TODO: make this use the main calc callsite and get the plotly data from there


def example_col():
    bar_size: BarSize = "#6"
    calc_props = getCalculatedColumnProps(bar_size)

    return Column(
        Input("w", 24),
        Input("h", 18),
        Input("bar_size", bar_size),
        Input("cover", 2),
        Input("nx", 5),
        Input("ny", 2),
        Input("f'_c", 8000),
        Input("f_y", 60),
        False,
        True,
        calc_props["A_b"],
        calc_props["E_s"],
        calc_props["e_c"],
    )


if __name__ == "__main__":
    col = example_col()

    # for each load case: P, Mx, My, and whether the calc should be shown
    load_data = [
        [300, 100, 200, "yes"],
        [-100, 50, -60, "no"],
        [1500, 300, -300, "no"],
    ]

    pmm_data = calculation(default_loads=load_data, col=col)

    fig = pmm_plotter_plotly.plot(pmm_data)

    fig.show()
