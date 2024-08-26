import point_search_ecc
import math
import try_axis_document
import show_dcr_calc
import try_axis


# accepts as arguments the column and the load point and returns
# the dcr for this particular load point
def get_dcr(col, load):
    target_M = math.sqrt(load[0] ** 2 + load[1] ** 2)
    target_ecc = math.atan2(load[2], target_M)

    # if the target eccentricity angle is almost vertical, return the DCR based on the

    tol = 0.1 * math.pi / 180
    if target_ecc > math.pi / 2 - tol:
        if load[3]:
            show_dcr_calc.show(True, load, col.max_phi_pn, 0)
        return load[2] / col.max_phi_pn
    if target_ecc < -math.pi / 2 + tol:
        if load[3]:
            show_dcr_calc.show(True, load, col.min_phi_pn, 0)
        return load[2] / col.min_phi_pn

    target_lambda = math.atan2(abs(load[1]), abs(load[0]))
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
    dcr = float("inf")
    if P != 0:
        dcrs[2] = load[2] / P
        dcr = dcrs[2]
    if Mx != 0:
        dcrs[0] = abs(load[0] / Mx)
        dcr = dcrs[0]
    if My != 0:
        dcrs[1] = abs(load[1] / My)
        dcr = dcrs[1]
    print("dcrs", dcrs)
    if load[3]:
        efficalc_capacity = try_axis_document.try_axis(
            col, final_guess[0], final_guess[1]
        )

        show_dcr_calc.show(False, load, efficalc_capacity, dcr)
    return dcr
