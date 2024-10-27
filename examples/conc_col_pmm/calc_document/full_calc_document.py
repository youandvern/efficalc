from ..calc_document.plotting import pure_mx_my_plotter
from ..col import assign_max_min
from ..col.col_canvas import draw_column_with_dimensions
from ..col.column import Column
from ..pmm_search.load_combo import LoadCombination
from .dcr_calc_runner import calc_dcrs
from .plotting.pmm_mesh import get_mesh
from .results_summary import results_summarizer


def calculation(
    col: Column,
    load_combos: list[LoadCombination],
):
    # draw the column cross-section with dimensions and callouts
    draw_column_with_dimensions.draw(col, "Section of Column")

    # calculate_axial_load_limits the max tension and compression to this column
    axial_limits = assign_max_min.calculate_axial_load_limits(col)

    # Retrieve the quarter PMM mesh, which has points
    # in the format (Mx, My, P).
    _, _, _, mesh = get_mesh(col, 48, 18, axial_limits)

    # show the PM curves for bending purely about the x and y axes
    pure_mx_my_plotter.plot(mesh)

    # calculate DCRs for all load cases
    dcr_results = calc_dcrs(load_combos, mesh, col, axial_limits)

    results_summarizer(load_combos, dcr_results)
