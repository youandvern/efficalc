import matplotlib.pyplot as plt
import math


def plot(capacity_pts, point):
    [phi_Mn, phi_Pn] = capacity_pts
    pt_lambda = math.atan2(point[1], point[0])  # the angle for the current point

    Muxy = math.sqrt(sum((point[i] ** 2 for i in range(2))))  # the biaxial moment

    pt_count = len(phi_Mn)  # how many points are plotted

    fig, ax = plt.subplots()

    plot_angle = str(round(pt_lambda * 180 / math.pi)) + "$\degree$"
    ax.set_title("P-M Interaction Diagram at $\lambda=$" + plot_angle)

    plt.plot(phi_Mn, phi_Pn, linewidth=2)

    ax.set_xlabel("${\phi}M_{nxy}$ (kip-ft)", fontsize=12)
    ax.set_ylabel("${\phi}P_{n}$ (kip)", fontsize=12)

    ax.grid(True, which="both")

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

    load_span = phi_Pn[-1] - phi_Pn[0]
    label_offsets = (max(phi_Mn) * 0.008, load_span * 0.02)
    # label the intersections with the y-axis
    for i in (0, pt_count - 1):
        pos = (phi_Mn[i], phi_Pn[i])
        label = str(round(phi_Pn[i], 1))
        plt.plot(pos[0], pos[1], marker="+", ms=12, mew=1.2, c="black")
        plt.text(pos[0] + label_offsets[0], pos[1] + label_offsets[1], label)

    # plot and label the load point
    pos = (Muxy, point[2])
    moment_label = "$M_{uxy}=$" + str(round(Muxy, 1)) + " kip-ft, "
    axial_label = "$P_u=$" + str(round(point[2], 1)) + " kip"
    label = moment_label + axial_label

    plt.plot(pos[0], pos[1], marker="+", ms=12, mew=1.2, c="red")
    plt.text(pos[0] + label_offsets[0], pos[1] + label_offsets[1], label)

    plt.show()
