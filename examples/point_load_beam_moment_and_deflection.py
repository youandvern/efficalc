from matplotlib import pyplot as plt

from efficalc import (
    Calculation,
    FigureFromMatplotlib,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
    ft_to_in,
    maximum,
    sqrt,
)
from efficalc.sections import ALL_AISC_WIDE_FLANGE_NAMES, get_aisc_wide_flange


def calculation():

    Title("Beam Moment and Deflection with Point Load")
    TextBlock(
        "Calculate the moment and deflection demands of a simply-supported steel beam due to a point load."
    )

    Heading("Inputs")
    L = Input("L", 20, "ft", "Beam length")
    F = Input("F", 15, "kips", "Point load force")
    x = Input("x", 4, "ft", "Point load position along the beam")
    size = Input(
        "size",
        "W12X40",
        description="Beam section size",
        input_type="select",
        select_options=ALL_AISC_WIDE_FLANGE_NAMES,
    )

    Heading("Moment Demand")
    Calculation("M_{max}", (F * x * brackets(L - x)) / L, "kip-ft")
    figure = draw_moment_diagram(L.get_value(), F.get_value(), x.get_value())
    FigureFromMatplotlib(figure)

    Heading("Deflection")

    Heading("Beam and Load Dimensions", head_level=2)
    a = Calculation(
        "a",
        maximum(x, L - x),
        "ft",
        "The longer distance from the location of the load to a beam support",
    )
    b = Calculation(
        "b",
        L - a,
        "ft",
        "The shorter distance from the location of the load to a beam support",
    )

    Heading("Section Properties", head_level=2)
    section = get_aisc_wide_flange(size.get_value())
    E = Calculation("E", 29000, "ksi", "Modulus of elasticity for steel")
    I = Calculation("I", section.Ix, "in^4", "Beam moment of inertia")

    Heading("Deflection Calculation", head_level=2)
    Calculation(
        "\delta_{max}",
        (F * a * b * brackets(a + 2 * b) * sqrt(3 * a * brackets(a + 2 * b)))
        / (27 * E * I * L)
        * ft_to_in**3,
        "in",
    )
    deflection_figure = draw_deflection_diagram(
        L.get_value(), F.get_value(), x.get_value(), E.get_value(), I.get_value()
    )
    FigureFromMatplotlib(deflection_figure)


def draw_moment_diagram(
    beam_length: float, load: float, load_position: float
) -> plt.Figure:
    # Define x values for the plot
    x_list = points_along_beam(beam_length, load_position, 10)

    # Calculate the moment for each plotted x position
    M_list = [
        (
            (load * x * (beam_length - load_position) / beam_length)
            if x <= load_position
            else (load * (beam_length - x) * load_position / beam_length)
        )
        for x in x_list
    ]

    # Plot the moment diagram
    fig, ax = set_up_plot(beam_length, "Moment (kip·ft)")

    ax.plot(x_list, M_list, label="Moment Diagram", color="blue")
    ax.fill_between(x_list, M_list, alpha=0.1, color="blue")  # Fill under the curve

    index_at_load = x_list.index(load_position)
    M_at_load = M_list[index_at_load]
    ax.plot(
        load_position, M_at_load, marker="o", color="red", label="Point Load Location"
    )

    style_plots()
    return fig


def draw_deflection_diagram(
    beam_length: float, load: float, load_position: float, E: float, I: float
) -> plt.Figure:

    # Define x values for the plot
    x_list = points_along_beam(beam_length, load_position, 100)

    # Calculate the deflection for each plotted x position
    x_list_in = [x * 12 for x in x_list]
    l = beam_length * 12
    a = load_position * 12
    b = l - a
    d_list = [
        (
            -load * b * x * (l**2 - b**2 - x**2) / (6 * E * I * l)
            if x <= a
            else (-load * a * (l - x)) * (2 * l * x - a**2 - x**2) / (6 * E * I * l)
        )
        for x in x_list_in
    ]

    # Plot the moment diagram
    fig, ax = set_up_plot(beam_length, "Deflection (in)")

    ax.plot(x_list, d_list, label="Deflection", color="blue")
    ax.fill_between(x_list, d_list, alpha=0.1, color="blue")  # Fill under the curve

    index_at_load = x_list.index(load_position)
    d_at_load = d_list[index_at_load]
    ax.plot(
        load_position, d_at_load, marker="o", color="red", label="Point Load Location"
    )

    style_plots()
    return fig


def set_up_plot(beam_length: float, y_label: str):
    fig, ax = plt.subplots(figsize=(10, 3))

    # Add a beam and point for the point load
    ax.plot([0, beam_length], [0, 0], color="black", label="Beam", linewidth=5)

    # Style the plot
    plt.xlabel("Position along the beam (ft)")
    plt.ylabel(y_label)
    return fig, ax


def style_plots():
    plt.grid(True)
    plt.legend()
    plt.subplots_adjust(bottom=0.25)


def points_along_beam(beam_length: float, load_position: float, n_steps: int):
    step_size = beam_length / (n_steps - 1)
    x_list = [step * step_size for step in range(n_steps)]
    x_list.append(load_position)
    x_list.sort()
    return x_list
