from examples.conc_col_pmm.col import assign_max_min, column
from .add_col_inputs_document import add_inputs
from .dcr_calc_runner import calc_dcrs
from .results_summary import results_summarizer

from efficalc import InputTable
from examples.conc_col_pmm.calc_document.plotting import (
    pmm_plotter_plotly,
    pure_mx_my_plotter,
)
from ..col.col_canvas import draw_column_with_dimensions
from examples.conc_col_pmm.constants.rebar_data import fy_dict


def calculation(
    col_data=[50, 70, "#9", 2, 4, 3, 11000, 60, False, False],
    load_table=InputTable(
        [[500, 300, 0, True]],
        ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "Show Calc in Report"],
        "Load Cases",
        False,
        False,
    ),
):
    # create a column object based on the inputs
    python_inputs = []
    for i in range(7):
        python_inputs.append(col_data[i].get_value())
    python_inputs.append(fy_dict[col_data[7].get_value()])
    python_inputs.extend(col_data[8:])
    col = column.Column(*python_inputs)

    # above were the efficalc Inputs we already have, and below some additional inputs and assumptions
    # are created and added to the calc report
    additional_inputs = add_inputs(col)

    # assign efficalc objects to this column for later use
    col_data[7] = additional_inputs[1]
    col_data[2] = additional_inputs[0]
    col_data = col_data[:8]
    col.efficalc_inputs = col_data + additional_inputs[2:]

    # draw the column cross-section with dimensions and callouts
    draw_column_with_dimensions.draw(col, "Section of Column")

    # assign the max tension and compression to this column
    assign_max_min.assign(col)

    # plot the PMM diagram and retrieve the quarter PMM mesh, which has points
    # in the format (Mx, My, P). The load table passed has data in the format
    # (P, Mx, My, show_calc)
    mesh, pmm_figure = pmm_plotter_plotly.plot(col, 48, 18, load_table.data)

    # show the PM curves for bending purely about the x and y axes
    pure_mx_my_plotter.plot(mesh)

    # calculate DCRs for all load cases
    dcr_results = calc_dcrs(load_table, mesh, col)

    results_summarizer(load_table, dcr_results)
