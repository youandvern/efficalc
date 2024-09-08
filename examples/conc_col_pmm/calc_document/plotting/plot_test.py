from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.col.assign_max_min import assign
from efficalc import (
    Heading,
    Input,
    InputTable,
)
from examples.conc_col_pmm.calc_document.add_col_inputs_document import add_inputs


from examples.conc_col_pmm.calc_document.plotting import pmm_plotter_plotly


example_data_1 = [10, 40, "#7", 1.5, 2, 10, 8000, 80, False, False]
example_data = [10, 40, "#7", 1.5, 2, 10, 8000, "80 ksi", "Edge", "Tied"]


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

_, fig = pmm_plotter_plotly.plot(col, 48, 18)

fig.show()
