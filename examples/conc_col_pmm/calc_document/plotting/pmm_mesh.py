import math

from ...col.axial_limits import AxialLimits
from ...col.column import Column
from ...pmm_search.load_search import bisect_load
from ...pmm_search.load_search.point_search_load import search


def get_mesh(col: Column, intervals, load_spaces, axial_limits: AxialLimits):
    # "intervals" is the number of spaces in the angle of eccentricity,
    # "load_spaces" is the number of vertical spaces in the PMM diagram
    # Returns a mesh containing all the points of the PMM diagram, plus
    # a quarter of that mesh

    # vectors containing the points to plot
    x = []
    y = []
    z = []

    # the bottom point must be added intervals+1 times because each level of
    # the mesh needs intervals+1 points in order to form a closed surface
    x.append([0] * (intervals + 1))
    y.append([0] * (intervals + 1))
    z.append([axial_limits.min_phi_pn] * (intervals + 1))

    vert_space = axial_limits.load_span / load_spaces
    c_guess = 0  # the starting guess for neutral axis

    quarter = math.floor(intervals / 4)  # number of angle spaces in one quadrant
    lambda_space = 2 * math.pi / intervals  # the change in angle between points
    theta_guesses = [-lambda_space * i for i in range(1, quarter)]  # the guess for
    # what theta should be at each point between the x and y axes, to be
    # updated at each vertical level
    count = 0

    quarter_mesh = [[0] * (quarter + 1) for i in range(load_spaces + 2)]  # a matrix
    # to contain the output points, with height (outer dimension) spanning all
    # the axial load interpolation points and width (inner dimension) spanning
    # from lambda=0 to lambda=90
    quarter_mesh[0] = [(0, 0, axial_limits.min_phi_pn) for i in range(quarter + 1)]
    quarter_mesh[load_spaces + 1] = [
        (0, 0, axial_limits.max_phi_pn) for i in range(quarter + 1)
    ]

    for vert_count in range(1, load_spaces + 1):
        count += 1
        c_guess += (col.w + col.h) / (2 * load_spaces)  # increment the guess for
        # the neutral axis depth
        load_target = axial_limits.min_phi_pn + vert_space * vert_count
        coords = [[0] * (intervals + 1) for i in range(3)]

        # get the output for theta=0 and apply it in 3 points
        out = bisect_load.bisect(col, [0, load_target], [0, c_guess], axial_limits)
        quarter_mesh[vert_count][0] = out[:3]
        for pos in (0, quarter * 2, quarter * 4):
            mult = [1 if (pos != quarter * 2) else -1, 1, 1]
            for j in range(3):
                coords[j][pos] = out[j] * mult[j]

        # get the output for theta=-90 and apply it in 2 points
        out = bisect_load.bisect(
            col, [math.pi / 2, load_target], [-math.pi / 2, c_guess], axial_limits
        )
        quarter_mesh[vert_count][quarter] = out[:3]
        for pos in (quarter, quarter * 3):
            mult = [1, 1 if pos == quarter else -1, 1]
            for j in range(3):
                coords[j][pos] = out[j] * mult[j]

        # iterate over the remaining possible neutral axis angles between 0
        # and -90 and for each one, add its point to the four quadrants of the
        # PMM diagram
        lambda_target = lambda_space  # the current target lambda
        for i in range(1, quarter):
            out = search(
                col,
                [lambda_target, load_target],
                [theta_guesses[i - 1], c_guess],
                axial_limits,
            )
            quarter_mesh[vert_count][i] = out[:3]
            theta_guesses[i - 1] = out[3]

            c_guess = out[4]
            indices = [
                i,
                quarter * 2 - i,
                quarter * 2 + i,
                intervals - i,
            ]  # the indices in
            # the vector "coords" corresponding to the current point
            for pos, index in enumerate(indices):
                mult = [1 if (pos == 0 or pos == 3) else -1, 1 if pos < 2 else -1, 1]
                for j in range(3):
                    coords[j][index] = out[j] * mult[j]
            lambda_target += lambda_space

        x.append(coords[0])
        y.append(coords[1])
        z.append(coords[2])

    x.append([0] * (intervals + 1))
    y.append([0] * (intervals + 1))
    z.append([axial_limits.max_phi_pn] * (intervals + 1))

    return x, y, z, quarter_mesh
