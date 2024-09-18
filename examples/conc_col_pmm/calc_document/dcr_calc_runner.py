from examples.conc_col_pmm.pmm_search.ecc_search.get_dcr_ecc import get_dcr_ecc
from examples.conc_col_pmm.calc_document.plotting import get_capacity, point_plotter
from efficalc import FigureFromMatplotlib, Heading


def calc_dcrs(load_table, mesh, col):
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
            capacity_pts = get_capacity.get_capacity(mesh, load)
            # plot the PM diagram for this point
            pm_figure = point_plotter.plot(capacity_pts, load, False)
            FigureFromMatplotlib(
                pm_figure, "PM interaction diagram for this load case. "
            )

        dcr_results.append(get_dcr_ecc(col, load))
    return dcr_results
