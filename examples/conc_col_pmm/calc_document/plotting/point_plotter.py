import math

import matplotlib.pyplot as plt

from ...pmm_search.load_combo import LoadCombination

"""
The function "plot" creates and returns a matplotlib figure showing a PM diagram. 

Parameters:

capacity_pts: a list of the capacity points on the PM curve, in the format 
(Mxy, P). 

point: the load point if this plot is for a DCR calculation, or None if this plot
is simply to show the PM curve aligned with the Mx or My axis. The point is in 
the format (P, Mx, My). 

only_Mx: boolean, and only used when point=None, True means this is for bending
in the x-direction. 
"""


def plot(capacity_pts, point: LoadCombination | None, only_Mx):
    [phi_Mn, phi_Pn] = capacity_pts

    if point:
        # get the lamdba for the load point
        pt_lambda = math.atan2(point.my, point.mx)  # the angle for the current point
    else:
        # set the lambda to the desired axis
        pt_lambda = 0 if only_Mx else math.pi / 2

    pt_count = len(phi_Mn)  # how many points are plotted

    fig, ax = plt.subplots()
    ax.grid(True, which="both", zorder=0, linewidth=0.4)
    # set the x-spine (see below for more info on `set_position`)
    ax.spines["left"].set_position("zero")

    # turn off the right spine/ticks
    ax.spines["right"].set_color("none")
    ax.yaxis.tick_left()

    # set the y-spine
    ax.spines["bottom"].set_position("zero")

    # turn off the top spine/ticks
    ax.spines["top"].set_color("none")
    ax.xaxis.tick_bottom()

    plot_angle = str(round(pt_lambda * 180 / math.pi)) + "$\degree$"
    ax.set_title("P-M Interaction Diagram at $\lambda=$" + plot_angle)

    plt.plot(phi_Mn, phi_Pn, linewidth=2, zorder=1)

    ax.set_xlabel("${\phi}M_{nxy}$ (kip-ft)", fontsize=12, zorder=2)
    ax.set_ylabel("${\phi}P_{n}$ (kip)", fontsize=12, zorder=2)

    ax.set_axisbelow(True)

    load_span = phi_Pn[-1] - phi_Pn[0]

    # define offset distances for axis labels depending on point
    label_offset_x = max(phi_Mn) * 0.008
    label_offsets_y=-load_span * 0.05, load_span * 0.02
    # label the intersections with the y-axis
    for i in (0, pt_count - 1):
        pos = (phi_Mn[i], phi_Pn[i])
        label = str(round(phi_Pn[i], 1))
        plt.plot(pos[0], pos[1], marker="+", ms=12, mew=1.2, c="black", zorder=3)
        label_offset_y=label_offsets_y[0] if i==0 else label_offsets_y[1]
        plt.text(pos[0] + label_offset_x, pos[1] + label_offset_y, label, zorder=3)

    if point:
        Muxy = math.sqrt(point.mx**2 + point.my**2)  # the biaxial moment

        # plot and label the load point
        pos = (Muxy, point.p)
        moment_label = "($M_{uxy}=$" + str(round(Muxy, 1)) + " kip-ft, "
        axial_label = "$P_u=$" + str(round(point.p, 1)) + " kip)"
        label = moment_label + "\n" + axial_label

        plt.plot(pos[0], pos[1], marker="+", ms=12, mew=1.2, c="red", zorder=4)
        label_offset_y = label_offsets_y[0] if i == 0 else label_offsets_y[1]
        plt.text(pos[0] + label_offset_x, pos[1] + label_offset_y, label, zorder=5)

        fig = ax.get_figure()

    return fig
