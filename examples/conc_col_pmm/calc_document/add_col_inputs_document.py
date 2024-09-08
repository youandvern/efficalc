from efficalc import Heading, Assumption, Calculation
from examples.conc_col_pmm.constants.rebar_data import fy_dict


def add_inputs(col):
    bar_area = Calculation(
        "A_{\\mathrm{bar}}", col.bar_area, "in^2", description="Area of one bar"
    )

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
