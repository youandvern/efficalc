import math

from examples.conc_col_pmm.calc_document.show_dcr_calc import show as show_dcr_calc
from examples.conc_col_pmm.calc_document.try_axis_document import try_axis_document
from examples.conc_col_pmm.col.axial_limits import AxialLimits
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.pmm_search.ecc_search import point_search_ecc
from examples.conc_col_pmm.pmm_search.load_combo import LoadCombination


# accepts as arguments the column and the load point and returns
# the dcr for this particular load point. The load point is formatted
# as (P, Mx, My).
def get_dcr_ecc(col: Column, load: LoadCombination, axial_limits: AxialLimits):
    target_M = math.sqrt(load.mx**2 + load.my**2)
    target_ecc = math.atan2(load.p, target_M)

    # if the target eccentricity angle is almost vertical, return the DCR based on the

    tol = 0.1 * math.pi / 180
    if target_ecc > math.pi / 2 - tol:
        if load.show_in_report:
            show_dcr_calc(True, load, axial_limits.max_phi_pn, 0)
        return load.p / axial_limits.max_phi_pn
    if target_ecc < -math.pi / 2 + tol:
        if load.show_in_report:
            show_dcr_calc(True, load, axial_limits.min_phi_pn, 0)
        return load.p / axial_limits.min_phi_pn

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
        efficalc_capacity = try_axis_document(
            col, axial_limits, final_guess[0], final_guess[1]
        )

        show_dcr_calc(False, load, efficalc_capacity, dcr)
    return dcr
