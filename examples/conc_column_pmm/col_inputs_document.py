from efficalc import (
    Heading,
    Input,
    Assumption,
)


def get_inputs(col):

    Heading("Column Inputs")
    w = Input("w", col.w, "in", description="Column section width (x dimension)")
    h = Input("h", col.h, "in", description="Column section height (y dimension)")
    Input("", "\\" + col.bar_size, "", description="Rebar size")
    bar_area = Input(
        "A_{\\mathrm{bar}}", col.bar_area, "in^2", description="Area of one bar"
    )
    bar_cover = Input("", col.bar_cover, "in", description="Rebar cover")

    cover_type = (
        "to\\ center\\ of\\ bar\\ (not\\ clear\\ cover)"
        if col.cover_to_center
        else "to\\ edge\\ of\\ bar\\ (clear\\ cover)"
    )
    Input("", cover_type, "", description="Rebar cover type")

    transverse_type = "Spiral" if col.spiral_reinf else "Tied"
    Input("", transverse_type, "", description="Transverse reinforcement type")

    bars_x = Input(
        "", col.bars_x, "", description="Number of bars on the top/bottom edges"
    )
    bars_y = Input(
        "", col.bars_y, "", description="Number of bars on the left/right edges"
    )
    fc = Input("f'_c", col.fc, "psi", description="Concrete strength")
    fy = Input("f_y", col.fy, "ksi", description="Steel strength")

    STEEL_E = Input(
        "E_s", 29000, "ksi", "Steel modulus of elasticity", "ACI 318-19 20.2.2.2"
    )
    CONC_EPSILON = Input(
        "\\epsilon_u", 0.003, "", "Concrete strain at f'c", "ACI 318-19 22.2.2.1"
    )

    Heading("Assumptions")
    Assumption("ACI 318-19 controls the design")
    Assumption("Reinforcement is non-prestressed")
    Assumption(
        "Lap splices of longitudinal reinforcement are in accordance with ACI 318-19 Table 10.7.5.2.2"
    )
    Assumption(
        "Strain in concrete and reinforcement is proportional to distance from the neutral axis, per ACI 318-19 22.2.1.2 "
    )

    return (
        w,
        h,
        bar_area,
        bar_cover,
        cover_type,
        transverse_type,
        bars_x,
        bars_y,
        fc,
        fy,
        STEEL_E,
        CONC_EPSILON,
    )
