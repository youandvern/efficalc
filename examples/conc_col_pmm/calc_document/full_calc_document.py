from examples.conc_col_pmm.pmm_search.ecc_search.get_dcr_ecc import get_dcr_ecc
from examples.conc_col_pmm.col import assign_max_min, column
from .add_col_inputs_document import add_inputs

from efficalc import FigureFromMatplotlib, Table, Heading, InputTable, Comparison
from examples.conc_col_pmm.calc_document.plotting import (
    pmm_plotter_plotly,
    point_plotter,
    get_capacity,
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

    draw_column_with_dimensions.draw(col, "Section of Column")

    # assign the max tension and compression to this column
    assign_max_min.assign(col)

    load_cases = load_table.data
    n = len(load_cases)
    load_cases = [
        [load_cases[i][1], load_cases[i][2], load_cases[i][0]] for i in range(n)
    ]

    mesh, pmm_figure = pmm_plotter_plotly.plot(col, 48, 18, load_cases)

    # show the PM curves for bending purely about the x and y axes
    Heading("PM Diagrams for Pure Mx and My")
    n = len(mesh)
    m = len(mesh[0])
    capacity_pts = [
        [mesh[i][0][0] for i in range(n)],
        [mesh[i][0][2] for i in range(n)],
    ]
    pm_figure = point_plotter.plot(capacity_pts, None, True)
    FigureFromMatplotlib(pm_figure, "PM interaction diagram for pure Mx.")

    capacity_pts = [
        [mesh[i][m - 1][1] for i in range(n)],
        [mesh[i][m - 1][2] for i in range(n)],
    ]
    pm_figure = point_plotter.plot(capacity_pts, None, False)
    FigureFromMatplotlib(pm_figure, "PM interaction diagram for pure My.")

    dcr_results = []
    for i in range(len(load_table.data)):
        load = load_table.data[i]
        if load[3]:  # show the full calculations for this load case
            Heading(
                "DCR Calculation for Load Case P="
                + str(round(load[0], 1))
                + ", Mx="
                + str(round(load[1], 1))
                + ", My="
                + str(round(load[2], 1))
            )
            load = [
                load[1],
                load[2],
                load[0],
                load[3],
            ]  # rearrange to be in the order Mx, My, P, then whether to show
            capacity_pts = get_capacity.get_capacity(mesh, load)
            # plot the PM diagram for this point
            pm_figure = point_plotter.plot(capacity_pts, load, False)
            FigureFromMatplotlib(
                pm_figure, "PM interaction diagram for this load case. "
            )

        dcr_results.append(get_dcr_ecc(col, load))

    Heading("Summary of Results")
    data = [
        load_table.data[i][:3]
        + [round(dcr_results[i], 2), "O.K." if dcr_results[i] < 1 else "N.G."]
        for i in range(len(load_table.data))
    ]

    headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "PM Vector DCR", "Passing?"]
    Table(data, headers, "DCRs For All Load Cases", False, False)

    # calculate the max DCR and show
    max_dcr = round(max(dcr_results), 2)
    Comparison(
        max_dcr,
        "<",
        1.0,
        true_message="O.K.",
        false_message="N.G.",
        description="Max DCR check:",
        result_check=True,
    )
