import point_search_ecc
import math
import sections
import col_inputs_document
from efficalc import Heading, Input, Assumption, TextBlock
import get_dcr_ecc
import max_tens_comp
from efficalc import Title, Calculation, Input, sqrt, FigureFromMatplotlib, Table
import pmm_plotter
import get_capacity
import point_plotter
import draw_column


def calculation(
    col_data=(50, 70, "#9", 2, 4, 3, 11000, 60, False, False),
    load_cases=[[100, 800, 2600, True], [0, 0, -2200, True]],
):
    Title("Calculation Report")

    col = sections.Column(*col_data)
    col.shear_bar_size = "#4"
    draw_column.draw_column_section(col, "Section of Column")
    # max compression and tension capacity
    (
        col.max_pn,
        col.max_phi_pn,
        col.min_pn,
        col.min_phi_pn,
        col.efficalc_inputs,
    ) = max_tens_comp.calculation(col)

    col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
    # maximum and minimum allowable loads, to be used for normalizing error

    mesh, pmm_figure = pmm_plotter.plot(col, 36, 12)

    dcr_results = []
    for i, load in enumerate(load_cases):
        if load[3]:
            Heading(
                "DCR Calculation for Load Case Mx="
                + str(round(load[0], 1))
                + ", My="
                + str(round(load[1], 1))
                + ", P="
                + str(round(load[2], 1))
            )
            capacity_pts = get_capacity.get_capacity(mesh, load)
            # plot the PM diagram for this point
            pm_figure = point_plotter.plot(capacity_pts, load)
            FigureFromMatplotlib(
                pm_figure, "PM interaction diagram for this load case. "
            )

        dcr_results.append(get_dcr_ecc.get_dcr(col, load))

    Heading("Summary of Results")
    data = [
        load_cases[i][:3]
        + [round(dcr_results[i], 2), "O.K." if dcr_results[i] < 1 else "N.G."]
        for i in range(len(load_cases))
    ]

    headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "PM Vector DCR", "Passing?"]
    Table(data, headers, "DCRs For All Load Cases", False, False)
