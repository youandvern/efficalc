import math
import rotate
import starting_pts
import limit_comp


def bisect(col, target, guess):
    # This function returns a point on the PMM diagram (Mx, My, and P) plus the
    # two inputs that produced that point (theta and c) as a tuple. The point
    # returned is intended to match the values in "target," which is a
    # list containing the target lambda and target factored axial load in that
    # order. "col" is the column being analyzed and "guess" contains the
    # starting guess of the theta and c necessary to produce target.

    tol = 0.005  # normalized error accepted as the actual point

    depth = col.w * math.sin(target[0]) + col.h * math.cos(target[0])  # the distance
    # between the section corners perpendicular to the neutral axis

    # set the two initial guess points
    pts = starting_pts.starting_pts(col, guess, depth, False, target)

    error = float("inf")  # normalized distance of the current point from the
    # target

    guess = [0] * 2  # the guess at each iteration
    change = [0] * 2  # the change in inputs between iterations
    best_error = 10  # record for normalized error, initialize to a large number
    best = []  # the point encountered so far with smallest normalized error

    counter = 0
    while error > tol and counter < 50:
        for i in range(2):
            # calculate an estimate of the rate of change of this output
            slope = (pts[1][i + 2] - pts[0][i + 2]) / (pts[1][i] - pts[0][i])

            # calculate the distance of this output from its target
            dist = target[i] - pts[1][i + 2]
            if slope != 0:  # check slope to avoid dividing by zero
                # move by the amount estimated to get to zero, minus a small
                # reduction for stability
                change[i] = dist / slope
            else:
                change[i] = 0
        # rotate the change vector so that it isn't horizontal or vertical
        change = rotate.rotate(change, depth, pts[1])

        error = float("inf")
        factor = 1  # factor for reducing the change between iterations

        # if the error increases after the first guess, the change should be
        # reduced to try to improve the guess
        while error > best_error and factor >= 0.1:
            for i in range(2):
                # calculate the next guess based on the current point
                guess[i] = pts[1][i] + change[i] * factor
            factor /= 5
            # limit both inputs to their bounds
            guess[0] = max(-math.pi / 2, min(0, guess[0]))
            guess[1] = max(1e-6, guess[1])

            # get the output for this guess, reducing c if the compression
            # is too high to
            (output, error, guess, add_count) = limit_comp.limit_comp(
                col, guess, target
            )
            counter += add_count

        # update the current and previous point
        pts[0] = pts[1]
        pts[1] = guess + [output[0]] + [output[3]]

        # update the lowest error and the best point if this guess is a record
        if error < best_error:
            best_error = error
            # the factored moments and axial force, plus the best guess inputs
            Mx = output[4] * math.cos(output[0])
            My = output[4] * math.sin(output[0])
            P = output[3]
            best = (Mx, My, P, pts[1][0], pts[1][1])
    return best
