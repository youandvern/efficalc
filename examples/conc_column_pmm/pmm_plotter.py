import matplotlib.pyplot as plt
import math
import numpy as np
import point_search
import bisect_load


def plot(col, intervals, load_spaces, plot):
    # This function plots the factored load capacity diagram for the column
    # col. "intervals" is the number of spaces in the angle of eccentricity,
    # "load_spaces" is the number of vertical spaces in the PMM diagram, and
    # "plot" is whether the 3D diagram should be plotted. Returns a mesh
    # containing all the points in one quadrant, from My=0 to Mx=0

    # vectors containing the points to plot
    x = []
    y = []
    z = []

    # the bottom point must be added intervals+1 times because each level of
    # the mesh needs intervals+1 points in order to form a closed surface
    x.append([0] * (intervals + 1))
    y.append([0] * (intervals + 1))
    z.append([col.min_phi_pn] * (intervals + 1))

    vert_span = col.max_phi_pn - col.min_phi_pn
    vert_space = vert_span / load_spaces
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
    quarter_mesh[0] = [(0, 0, col.min_phi_pn) for i in range(quarter + 1)]
    quarter_mesh[load_spaces + 1] = [(0, 0, col.max_phi_pn) for i in range(quarter + 1)]

    for vert_count in range(1, load_spaces + 1):
        count += 1
        c_guess += (col.w + col.h) / (2 * load_spaces)  # increment the guess for
        # the neutral axis depth
        load_target = col.min_phi_pn + vert_space * vert_count
        coords = [[0] * (intervals + 1) for i in range(3)]

        # get the output for theta=0 and apply it in 3 points
        out = bisect_load.bisect(col, [0, load_target], [0, c_guess])
        quarter_mesh[vert_count][0] = out[:3]
        for pos in (0, quarter * 2, quarter * 4):
            mult = [1 if (pos != quarter * 2) else -1, 1, 1]
            for j in range(3):
                coords[j][pos] = out[j] * mult[j]

        # get the output for theta=-90 and apply it in 2 points
        out = bisect_load.bisect(
            col, [math.pi / 2, load_target], [-math.pi / 2, c_guess]
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
            out = point_search.search(
                col, [lambda_target, load_target], [theta_guesses[i - 1], c_guess]
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

    if plot:
        x.append([0] * (intervals + 1))
        y.append([0] * (intervals + 1))
        z.append([col.max_phi_pn] * (intervals + 1))

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        ax = plt.axes(projection="3d")

        # set the aspect ratio so that Mx and My will be proportional
        ax.set_box_aspect((np.ptp(x), np.ptp(y), 0.6 * np.ptp(z)))

        ax.plot_surface(x, y, z, cmap="viridis", edgecolor="green")
        ax.set_title("PMM Diagram")

        ax.zaxis.set_rotate_label(False)
        ax.set_xlabel("${\phi}M_{nx}$", fontsize=12, rotation=0)
        ax.set_ylabel("${\phi}M_{ny}$", fontsize=12, rotation=0)
        ax.set_zlabel("${\phi}P_n$", fontsize=12, rotation=0)
        plt.show()
    return quarter_mesh
