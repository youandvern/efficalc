import pytest

from efficalc import Calculation, Input
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.constants.concrete_data import MAX_CONCRETE_STRAIN
from examples.conc_col_pmm.constants.rebar_data import STEEL_E, BarSize, rebar_area
from examples.conc_col_pmm.pmm_search.load_combo import LoadCombination


def getCalculatedColumnProps(bar_size: BarSize):
    A_b = Calculation("Ab", rebar_area(bar_size))

    E_s = Calculation("E_s", STEEL_E)
    e_c = Calculation(
        "\\epsilon_u",
        MAX_CONCRETE_STRAIN,
    )

    return {"A_b": A_b, "E_s": E_s, "e_c": e_c}


@pytest.fixture
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


@pytest.fixture
def loads():
    # for each load case: P, Mx, My, and whether the calc should be shown
    loads = [[300, 100, 200, True], [-100, 50, -60, False], [11500, 300, -300, False]]
    return [LoadCombination(*load) for load in loads]


@pytest.fixture
def example_col2():
    bar_size: BarSize = "#8"
    calc_props = getCalculatedColumnProps(bar_size)

    return Column(
        Input("w", 16),
        Input("h", 20),
        Input("bar_size", bar_size),
        Input("cover", 2.5),
        Input("nx", 3),
        Input("ny", 4),
        Input("f'_c", 6000),
        Input("f_y", 60),
        True,
        False,
        calc_props["A_b"],
        calc_props["E_s"],
        calc_props["e_c"],
    )


@pytest.fixture
def example_col3():
    bar_size: BarSize = "#8"
    calc_props = getCalculatedColumnProps(bar_size)

    return Column(
        Input("w", 24),
        Input("h", 36),
        Input("bar_size", bar_size),
        Input("cover", 1.5),
        Input("nx", 3),
        Input("ny", 4),
        Input("f'_c", 4000),
        Input("f_y", 40),
        False,
        False,
        calc_props["A_b"],
        calc_props["E_s"],
        calc_props["e_c"],
    )
