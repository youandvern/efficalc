from ...col.axial_limits import AxialLimits
from ...col.column import Column
from .limit_comp_load import limit_comp

reduction = 0.005  # the fraction of the total estimated span of both inputs
# that should be added/subtracted to the starting guess points


# Returns a list of two points which are the starting guesses for a gradient
# descent problem, where the two points are close together, centered on the
# supplied guess "guess," and different in both their theta and c values.
# "depth" is an estimate of the maximum c, and load_only is boolean, where
# True indicates that only the load should be varied
def starting_pts(col: Column, guess, depth, target, axial_limits: AxialLimits):
    # calculate the starting differences in theta and c between two points
    c_change = reduction * depth
    change_factors = (-1, 1)  # factors used to decrease parameters for A and to
    # increase parameters for B

    pts = [guess.copy() for i in range(2)]

    for i, factor in enumerate(change_factors):
        pts[i][1] += c_change * factor
        guess[1] = max(1e-6, guess[1])

        # calculate and store the load output for the current guess point
        output, error = limit_comp(col, pts[i], target, axial_limits)
        pts[i].extend([output[0], output[3]])
    return pts
