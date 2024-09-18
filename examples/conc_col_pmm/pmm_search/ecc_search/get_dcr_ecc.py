from examples.conc_col_pmm.pmm_search.ecc_search import point_search_ecc
import math
from examples.conc_col_pmm.calc_document.try_axis_document import try_axis_document
from examples.conc_col_pmm.calc_document.show_dcr_calc import show as show_dcr_calc


# accepts as arguments the column and the load point and returns
# the dcr for this particular load point. The load point is formatted
# as (P, Mx, My).
def get_dcr_ecc(col, load):
    target_M = math.sqrt(load[1] ** 2 + load[2] ** 2)
    target_ecc = math.atan2(load[0], target_M)

    # if the target eccentricity angle is almost vertical, return the DCR based on the

    tol = 0.1 * math.pi / 180
    if target_ecc > math.pi / 2 - tol:
        if load[3]:
            show_dcr_calc(True, load, col.max_phi_pn, 0)
        return load[0] / col.max_phi_pn
    if target_ecc < -math.pi / 2 + tol:
        if load[3]:
            show_dcr_calc(True, load, col.min_phi_pn, 0)
        return load[0] / col.min_phi_pn

    target_lambda = math.atan2(abs(load[2]), abs(load[1]))
    target = (target_lambda, target_ecc)

    # the best guess of theta is -lambda
    guess = [
        -target_lambda,
        (col.w + col.h) / 2,
    ]

    # find the point on the PMM diagram that is on the same vector as the
    # applied load
    Mx, My, P, final_guess = point_search_ecc.search(col, target, guess)

    dcrs = [float("inf")] * 3
    dcr_candidates = []
    if P != 0:
        dcrs[0] = load[0] / P
        dcr_candidates.append(load[0] / P)
    if Mx != 0:
        dcrs[1] = abs(load[1] / Mx)
        dcr_candidates.append(abs(load[1] / Mx))
    if My != 0:
        dcrs[2] = abs(load[2] / My)
        dcr_candidates.append(abs(load[2] / My))
    dcr = max(dcr_candidates) if len(dcr_candidates) > 0 else 0
    if load[3]:
        efficalc_capacity = try_axis_document(col, final_guess[0], final_guess[1])

        show_dcr_calc(False, load, efficalc_capacity, dcr)
    return dcr
