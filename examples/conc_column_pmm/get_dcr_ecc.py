import point_search_ecc
import math


# accepts as arguments the column and the load point and returns
# the dcr for this particular load point
def get_dcr(col, load):
    target_M = math.sqrt(load[0] ** 2 + load[1] ** 2)
    target_ecc = math.atan2(load[2], target_M)

    # if the target eccentricity angle is almost vertical, return the DCR based on the

    tol = 0.5 * math.pi / 180
    if target_ecc > math.pi / 2 - tol:
        return load[2] / col.max_phi_pn
    if target_ecc < -math.pi / 2 + tol:
        return load[2] / col.min_phi_pn

    target_lambda = math.atan2(abs(load[1]), abs(load[0]))
    target = (target_lambda, target_ecc)

    # the best guess of theta is -lambda, and the best guess of c is
    # based on the target load
    guess = [
        -target_lambda,
        (col.w + col.h) / (2 * (load[2] - col.min_phi_pn) / col.load_span),
    ]

    # find the point on the PMM diagram that is on the same vector as the
    # applied load
    print("guess", guess)
    Mx, My, P = point_search_ecc.search(col, target, guess)
    print("P", P, load[2])

    print("Mx", Mx, load[0])
    print("My", My, load[1])
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
    return dcr
