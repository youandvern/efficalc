from efficalc import FigureFromMatplotlib, Heading
from examples.conc_col_pmm.calc_document.plotting import get_capacity, point_plotter
from examples.conc_col_pmm.col.axial_limits import AxialLimits
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.pmm_search.ecc_search.get_dcr_ecc import get_dcr_ecc
from examples.conc_col_pmm.pmm_search.load_combo import LoadCombination


def calc_dcrs(
    load_combos: list[LoadCombination], mesh, col: Column, axial_limits: AxialLimits
):
    dcr_results = []
    for load in load_combos:
        if load.show_in_report:  # show the full calculations for this load case
            Heading(
                "DCR Calculation for Load Case P="
                + str(round(load.p, 1))
                + ", Mx="
                + str(round(load.mx, 1))
                + ", My="
                + str(round(load.my, 1))
            )
            capacity_pts = get_capacity.get_capacity(mesh, load)
            # plot the PM diagram for this point
            pm_figure = point_plotter.plot(capacity_pts, load, False)
            FigureFromMatplotlib(
                pm_figure, "PM interaction diagram for this load case. "
            )

        dcr_results.append(get_dcr_ecc(col, load, axial_limits))
    return dcr_results
