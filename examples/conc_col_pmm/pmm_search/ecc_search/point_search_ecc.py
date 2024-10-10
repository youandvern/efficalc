import math

from ...col.axial_limits import AxialLimits
from ...col.column import Column
from . import change_ecc, limit_comp_ecc

"""
Searches for a point on the PMM diagram with a certain lambda and eccentricity. 
Parameters: the column object, the target (as a tuple of lambda, then axial load), and the 
initial guess (as a tuple of theta, then neutral axis depth)
Returns: Mx, My, P, and the final guess as a two-value list
*the angle of eccentricity guess must be between 0 and -pi/2 and the target lambda
must be between 0 and pi/2
"""


# the purpose of this function is to search for a point with a particular lambda and eccentricity
def search(col: Column, target, guess, axial_limits: AxialLimits):
    tol = 0.001  # error accepted as the actual point

    # get output for the initial guess point
    output, error = limit_comp_ecc.limit_comp(col, guess, target, axial_limits)

    count = 1  # count of iterations (calls to "try_axis")
    count_lim = 100  # iteration limit

    while error > tol and count < count_lim:
        # get a descent direction for the current point
        direction, error = change_ecc.change(col, guess, target, output, axial_limits)

        # since finding the direction requires two "try_axis" calls
        count += 2

        # the factor to be applied to the change direction
        factor = 1

        # try the guess point and decrease "factor" until the error is less
        # than the error from the last point
        error2 = error + 1
        while error2 > error and factor > 0.01:
            guess2 = [guess[i] + factor * direction[i] for i in range(2)]

            output, error2 = limit_comp_ecc.limit_comp(
                col, guess2, target, axial_limits
            )
            # if "limit_comp" resulted in a change in the guess of c, update
            # the change factor to save calls to "try_axis" in the next
            # iteration. Since "guess2" was passed to "limit_comp", it is
            # already updated
            if guess2[1] != guess[1] + factor * direction[1] and direction[1] != 0:
                factor = (guess2[1] - guess[1]) / direction[1]

            count += 1
            factor *= 0.6

        guess = guess2
        error = error2

    # return the forces at the final trial point
    Mx = output[4] * math.cos(output[0])
    My = output[4] * math.sin(output[0])

    # it is possible that the point will be on the top plateau, so the
    # axial force must be limited
    P = min(axial_limits.max_phi_pn, output[3])
    return Mx, My, P, guess
