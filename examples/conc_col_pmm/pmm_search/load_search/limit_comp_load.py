import math

from ...col.axial_limits import AxialLimits
from ...col.column import Column
from ...struct_analysis import try_axis
from ..load_search.get_error_load import get_error


def limit_comp(col: Column, guess, target, axial_limits: AxialLimits):
    guess[0] = min(0, max(guess[0], -math.pi / 2))
    guess[1] = max(1e-6, guess[1])
    #  guess[1]=max(c_lims[0],max(c_lims[1],guess[1]))
    output = try_axis.try_axis(col, guess[0], guess[1], axial_limits)
    lim_factor = 0.999
    while output[3] > lim_factor * col.PHI_COMP * axial_limits.max_pn:
        # the current phi_pn (without the 0.8) is at or almost at its
        # maximum value, which means the column is probably in full
        # compression, which must be avoided or derivatives will be zero
        guess[1] /= 2
        output = try_axis.try_axis(col, guess[0], guess[1], axial_limits)
    while output[3] < lim_factor * axial_limits.min_phi_pn:
        # the current phi_pn is at or almost at its minimum value, so c must
        # b increased
        guess[1] *= 10
        output = try_axis.try_axis(col, guess[0], guess[1], axial_limits)
    # update the distance from the target point
    error = get_error(output, target, axial_limits.load_span)
    return output, error
