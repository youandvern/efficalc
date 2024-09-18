import pytest
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.col.assign_max_min import assign
from efficalc import (
    Input,
)
from examples.conc_col_pmm.calc_document.add_col_inputs_document import add_inputs


# inputs for the example column
example_data_1 = [24, 18, "#5", 1.5, 5, 4, 8000, 80, False, False]
example_data = [24, 18, "#5", 1.5, 5, 4, 8000, "80 ksi", "Edge", "Tied"]


# for each load case: P, Mx, My, and whether the calc should be shown
load_cases = [[300, 100, 200, True], [-100, 50, -60, False], [11500, 300, -300, False]]


@pytest.fixture
def example_col():
    col = Column(*example_data_1)

    w = Input("w", example_data[0])
    h = Input("h", example_data[1])
    # zero spaces
    bar_size = Input("", example_data[2])

    bar_cover = Input(" ", example_data[3])

    bars_x = Input("    ", example_data[4])
    bars_y = Input("     ", example_data[5])
    fc = Input("f'_c", example_data[6])
    fy = Input("f_y", example_data[7])

    col_data = [w, h, bar_size, bar_cover, bars_x, bars_y, fc, fy]
    # above were the efficalc Inputs we already have, and below some additional inputs and assumptions
    # are created and added to the calc report
    additional_inputs = add_inputs(col)

    # assign efficalc objects to this column for later use
    col_data[7] = additional_inputs[1]
    col_data[2] = additional_inputs[0]
    col.efficalc_inputs = col_data + additional_inputs[2:]

    assign(col)
    col.shear_bar_size = "#4"

    return col


@pytest.fixture
def col_data():
    return example_data


@pytest.fixture
def loads():
    return load_cases


example_data_2 = [16, 20, "#8", 2.5, 3, 4, 6000, 60, True, False]
example_data2 = [16, 20, "#8", 2.5, 3, 4, 6000, "60 ksi", True, False]


@pytest.fixture
def example_col2():
    example_data = example_data2
    col = Column(*example_data_2)

    w = Input("w", example_data[0])
    h = Input("h", example_data[1])
    # zero spaces
    bar_size = Input("", example_data[2])

    bar_cover = Input(" ", example_data[3])

    bars_x = Input("    ", example_data[4])
    bars_y = Input("     ", example_data[5])
    fc = Input("f'_c", example_data[6])
    fy = Input("f_y", example_data[7])

    col_data = [w, h, bar_size, bar_cover, bars_x, bars_y, fc, fy]
    # above were the efficalc Inputs we already have, and below some additional inputs and assumptions
    # are created and added to the calc report
    additional_inputs = add_inputs(col)

    # assign efficalc objects to this column for later use
    col_data[7] = additional_inputs[1]
    col_data[2] = additional_inputs[0]
    col.efficalc_inputs = col_data + additional_inputs[2:]

    assign(col)
    col.shear_bar_size = "#4"

    return col


example_data_3 = [24, 36, "#8", 1.5, 3, 4, 4000, 40, False, False]
example_data3 = [24, 36, "#8", 1.5, 3, 4, 4000, "40 ksi", False, False]


@pytest.fixture
def example_col3():
    example_data = example_data3
    col = Column(*example_data_3)

    w = Input("w", example_data[0])
    h = Input("h", example_data[1])
    # zero spaces
    bar_size = Input("", example_data[2])

    bar_cover = Input(" ", example_data[3])

    bars_x = Input("    ", example_data[4])
    bars_y = Input("     ", example_data[5])
    fc = Input("f'_c", example_data[6])
    fy = Input("f_y", example_data[7])

    col_data = [w, h, bar_size, bar_cover, bars_x, bars_y, fc, fy]
    # above were the efficalc Inputs we already have, and below some additional inputs and assumptions
    # are created and added to the calc report
    additional_inputs = add_inputs(col)

    # assign efficalc objects to this column for later use
    col_data[7] = additional_inputs[1]
    col_data[2] = additional_inputs[0]
    col.efficalc_inputs = col_data + additional_inputs[2:]

    assign(col)
    col.shear_bar_size = "#4"

    return col
