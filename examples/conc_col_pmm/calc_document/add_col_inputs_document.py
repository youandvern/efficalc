from efficalc import Heading, Assumption, Calculation
from examples.conc_col_pmm.constants.rebar_data import fy_dict


def add_inputs(col):
    """
    Heading("Column Inputs")
    w = Input("w", w, "in", description="Column section width (x dimension)")
    h = Input("h", h, "in", description="Column section height (y dimension)")
    Input("", "\\" + bar_size, "", description="Rebar size")
    """
    bar_area = Calculation(
        "A_{\\mathrm{bar}}", col.bar_area, "in^2", description="Area of one bar"
    )
    """
    bar_cover = Input("", col.bar_cover, "in", description="Rebar cover")
    
    cover_type = (
        "to\\ center\\ of\\ longitudinal\\ bar\\ (not\\ clear\\ cover)"
        if col.cover_to_center
        else "to\\ edge\\ of\\ longitudinal\\ bar\\ (clear\\ cover)"
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
    """
    STEEL_E = Calculation(
        "E_s", 29000, "ksi", "Steel modulus of elasticity", "ACI 318-19 20.2.2.2"
    )
    CONC_EPSILON = Calculation(
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

    # needed for drawing
    col.shear_bar_size = "#4"

    fy = Calculation("f_y", col.fy, "ksi")
    return [bar_area, fy, STEEL_E, CONC_EPSILON]
