import math

from latexexpr_efficalc import Variable

from ...calc_document.column_capacities import ColumnCapacities
from ...calc_document.show_dcr_calc import show as show_dcr_calc
from ...calc_document.try_axis_document import try_axis_document
from ...col.axial_limits import AxialLimits
from ...col.column import Column
from ..load_combo import LoadCombination
from . import point_search_ecc


# accepts as arguments the column and the load point and returns
# the dcr for this particular load point.
def get_dcr_ecc(col: Column, load: LoadCombination, axial_limits: AxialLimits):
    target_M = math.sqrt(load.mx**2 + load.my**2)
    target_ecc = math.atan2(load.p, target_M)

    tol = 0.01 * math.pi / 180
    # Load case is in pure tension
    if target_ecc > math.pi / 2 - tol:
        if load.show_in_report:
            capacities = ColumnCapacities(
                Variable("{\\phi}M_{nx}", 0, "kip-ft"),
                Variable("{\\phi}M_{ny}", 0, "kip-ft"),
                axial_limits.max_phi_pn_calculation,
            )
            show_dcr_calc(load, capacities)
        return load.p / axial_limits.max_phi_pn

    # Load case is in pure compression
    if target_ecc < -math.pi / 2 + tol:
        if load.show_in_report:
            capacities = ColumnCapacities(
                Variable("{\\phi}M_{nx}", 0, "kip-ft"),
                Variable("{\\phi}M_{ny}", 0, "kip-ft"),
                axial_limits.min_phi_pn_calculation,
            )
            show_dcr_calc(load, capacities)
        return load.p / axial_limits.min_phi_pn

    # Load has a bending moment component
    target_lambda = math.atan2(abs(load.my), abs(load.mx))
    target = (target_lambda, target_ecc)

    # the best guess of theta is -lambda
    guess = [
        -target_lambda,
        (col.w + col.h) / 2,
    ]

    # find the point on the PMM diagram that is on the same vector as the
    # applied load
    Mx, My, P, final_guess = point_search_ecc.search(col, target, guess, axial_limits)

    dcrs = [float("inf")] * 3
    dcr_candidates = []
    if P != 0:
        dcrs[0] = load.p / P
        dcr_candidates.append(load.p / P)
    if Mx != 0:
        dcrs[1] = abs(load.mx / Mx)
        dcr_candidates.append(abs(load.mx / Mx))
    if My != 0:
        dcrs[2] = abs(load.my / My)
        dcr_candidates.append(abs(load.my / My))
    dcr = max(dcr_candidates) if len(dcr_candidates) > 0 else 0
    if load.show_in_report:
        capacities = try_axis_document(
            col, axial_limits, final_guess[0], final_guess[1]
        )

        show_dcr_calc(load, capacities)
    return dcr
