from examples.conc_col_pmm.pmm_search.load_search.get_error_load import get_error
from examples.conc_col_pmm.struct_analysis import try_axis
import math


def limit_comp(col, guess, target):
    guess[0] = min(0, max(guess[0], -math.pi / 2))
    guess[1] = max(1e-6, guess[1])
    #  guess[1]=max(c_lims[0],max(c_lims[1],guess[1]))
    output = try_axis.try_axis(col, guess[0], guess[1])
    lim_factor = 0.999
    while output[3] > lim_factor * col.PHI_COMP * col.max_pn:
        # the current phi_pn (without the 0.8) is at or almost at its
        # maximum value, which means the column is probably in full
        # compression, which must be avoided or derivatives will be zero
        guess[1] /= 2
        output = try_axis.try_axis(col, guess[0], guess[1])
    while output[3] < lim_factor * col.min_phi_pn:
        # the current phi_pn is at or almost at its minimum value, so c must
        # b increased
        guess[1] *= 10
        output = try_axis.try_axis(col, guess[0], guess[1])
    # update the distance from the target point
    error = get_error(output, target, col.load_span)
    return output, error
