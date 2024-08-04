import math


def normal(vec, depth):
    # normalize this vector within the expected range of inputs
    return [vec[0] / (math.pi / 2), vec[1] / depth]


def de_normal(vec, depth):
    # reverse normalize
    return [vec[0] * (math.pi / 2), vec[1] * depth]


def rotate(change, depth, second_pt):
    norm = normal(change, depth)
    # calculate the angle of the current guess shifted to a 0-90 range
    # anything higher than 5 seems to cause slow convergence
    change_angle = math.atan2(norm[1], norm[0]) % (math.pi / 2)

    angle_tol = 5 * math.pi / 180  # the closeness of the guess to a vertical or
    # horizontal line allowable without correcting

    if change_angle < angle_tol or math.pi / 2 - change_angle < angle_tol:
        if not change_angle < angle_tol:
            angle_tol *= -1
        # rotate the change vector by angle_tol away from the nearest axis
        norm = [
            norm[0] * math.cos(angle_tol) - norm[1] * math.sin(angle_tol),
            norm[1] * math.cos(angle_tol) + norm[0] * math.sin(angle_tol),
        ]

    # it is possible that the rotation just made will be corrected when the
    # guess point is min/maxed with the bounds, so don't allow that to result
    # in divide by zero because two consecutive points have the same input
    if second_pt[1] == 1e-6:
        # the most recent guess for c is zero, so go up
        norm[1] = max(norm[1], 1e-4)
    if second_pt[0] == 0:
        # the most recent guess for theta is zero, so go down
        norm[0] = min(norm[0], -1e-4)
    elif second_pt[0] == -math.pi / 2:
        # the most recent guess for theta is -90, so go up
        norm[0] = max(norm[0], 1e-4)
    change_angle = math.atan2(norm[1], norm[0]) % (math.pi / 2)

    return de_normal(norm, depth)
