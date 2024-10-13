import math

from ...col.axial_limits import AxialLimits
from ...col.column import Column
from .limit_comp_load import limit_comp
from .starting_pts import starting_pts


def bisect(col: Column, target, guess, axial_limits: AxialLimits):
    # This function returns a point on the PMM diagram (Mx, My, and P) plus the
    # two inputs that produced that point (theta and c) as a tuple. The point
    # returned is intended to match the values in "target," which is a
    # list containing the target lambda and target factored axial load in that
    # order. "col" is the column being analyzed and "guess" contains the
    # starting guess for c. In this function, c is the only input varied,
    # and theta is held constant. This is because this function is intended
    # for points on the PMM diagram where it is known that lambda=-theta,
    # which occur on the positive and negative x and y axes.

    tol = 0.005  # normalized error accepted as the actual point

    depth = col.w * math.sin(target[0]) + col.h * math.cos(target[0])  # the distance
    # between the section corners perpendicular to the neutral axis

    # set the two initial guess points
    pts = starting_pts(col, guess, depth, target, axial_limits)

    error = float("inf")  # normalized distance of the current point from the
    # target

    guess = 0  # the guess for c at each iteration
    change = 0  # the change in c between iterations
    best_error = 10  # record for normalized error, initialize to a large number
    best = []  # the point encountered so far with smallest normalized error

    # debug:
    points = []
    points.append(pts[0])
    points.append(pts[1])

    counter = 0
    while error > tol and counter < 50:
        slope = (pts[1][3] - pts[0][3]) / (pts[1][1] - pts[0][1])

        # calculate the distance of this output from its target
        dist = target[1] - pts[1][3]
        if slope != 0:  # check slope to avoid dividing by zero
            # move by the amount estimated to get to zero, minus a small
            # reduction for stability
            change = dist / slope
        else:
            change = 0

        error = float("inf")
        factor = 1  # factor for reducing the change between iterations

        # if the error increases after the first guess, the change should be
        # reduced to try to improve the guess
        while error > best_error and factor >= 0.1 and counter < 50:
            # calculate the next guess based on the current point
            guess = pts[1][1] + change * factor
            factor /= 10
            # set the floor to avoid guesses that are zero or negative and to
            # avoid setting the guess equal to the current point
            guess_floor = 1e-6 if pts[1][1] != 1e-6 else 0.1
            guess = max(guess_floor, guess)

            # get the output for this guess, reducing c if the compression
            # is too high to
            output, error = limit_comp(
                col, [-target[0]] + [guess], target, axial_limits
            )
            counter += 1

        # update the current and previous point
        pts[0] = pts[1]
        pts[1] = [-target[0]] + [guess] + [output[0]] + [output[3]]
        points.append(pts[1])

        # update the lowest error and the best point if this guess is a record
        if error < best_error:
            best_error = error
            # the factored moments and axial force, plus the best guess inputs
            Mx = output[4] * math.cos(output[0])
            My = output[4] * math.sin(output[0])
            P = output[3]
            best = (Mx, My, P, pts[1][0], pts[1][1])

    return best
