import math
import change
import limit_comp


def search(col, target, guess):
    tol = 0.001  # error accepted as the actual point

    # get output for the initial guess point
    output, error = limit_comp.limit_comp(col, guess, target)

    count = 1  # count of iterations (calls to "try_axis")
    count_lim = 100  # iteration limit

    while error > tol and count < count_lim:
        # get a descent direction for the current point
        direction, error = change.change(col, guess, target, output)

        # since finding the direction requires two "try_axis" calls
        count += 2

        # the factor to be applied to the change direction
        factor = 1

        # try the guess point and decrease "factor" until the error is less
        # than the error from the last point
        error2 = error + 1
        while error2 > error and factor > 0.01:
            guess2 = [guess[i] + factor * direction[i] for i in range(2)]

            output, error2 = limit_comp.limit_comp(col, guess2, target)

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
    P = output[3]
    return Mx, My, P, guess[0], guess[1]
