from efficalc import Assumption, Calculation, Heading, Input, InputTable, Title
from examples.conc_col_pmm.constants.rebar_data import (
    REBAR_SIZES,
    REBAR_STRENGTHS,
    STEEL_E,
    rebar_area,
)

from ..col.column import Column
from ..constants.concrete_data import MAX_CONCRETE_STRAIN
from ..pmm_search.load_combo import LoadCombination
from .full_calc_document import calculation as full_calc

# TODO: this should return all info needed to plot visual tests, possibly take input params for defaults


# this function accepts inputs from the user and passes them to "full_calc_document"
def calculation(default_loads: list[list] = [[3000, -200, 100, True]]):
    Title("Concrete Column Biaxial Bending Calculation Report")

    Heading("Column Inputs")
    w = Input("w", 24, "in", description="Column section width (x dimension)")
    h = Input("h", 36, "in", description="Column section height (y dimension)")

    # zero spaces
    bar_size = Input(
        "",
        REBAR_SIZES[5],
        "",
        description="Longitudinal rebar size (Imperial)",
        input_type="select",
        select_options=REBAR_SIZES,
    )

    # one space
    bar_cover = Input(" ", 2, "in", description="Longitudinal rebar cover")

    # TODO: should clear cover account for the shear reinforcement?
    cover_options = [
        "Center",
        "Edge",
    ]

    # 2 spaces
    cover_type = Input(
        "  ",
        default_value=cover_options[1],
        unit="",
        description="Cover is to bar center or bar edge (clear cover)",
        input_type="select",
        select_options=cover_options,
    )
    transverse_options = ["Spiral", "Tied"]
    # 3 spaces
    transverse_type = Input(
        "   ",
        default_value=transverse_options[1],
        unit="",
        description="Transverse reinforcement type",
        input_type="select",
        select_options=transverse_options,
    )

    # 4 spaces
    bars_x = Input(
        "    ",
        6,
        "",
        description="Number of bars on the top/bottom edges",
        num_step=1,
    )

    # 5 spaces
    bars_y = Input(
        "     ",
        8,
        "",
        description="Number of bars on the left/right edges",
        num_step=1,
    )
    fc = Input("f^{\prime}_c", 8000, "psi", description="Concrete strength")

    fy = Input(
        "f_y",
        REBAR_STRENGTHS[1],
        "ksi",
        description="Steel strength",
        input_type="select",
        select_options=REBAR_STRENGTHS,
    )

    headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "Show Calc in Report"]
    load_table = InputTable(default_loads, headers, "Load Cases", False, False)

    load_combos = [
        LoadCombination(load[0], load[1], load[2], load[3]) for load in load_table.data
    ]

    # above were the efficalc Inputs from the user, and below, some additional inputs and assumptions
    # are created and added to the calc report

    A_b = Calculation(
        "A_{\\mathrm{bar}}",
        rebar_area(bar_size.get_value()),
        "in^2",
        description="Area of one bar",
    )

    E_s = Calculation(
        "E_s", STEEL_E, "ksi", "Steel modulus of elasticity", "ACI 318-19 20.2.2.2"
    )
    e_c = Calculation(
        "\\epsilon_u",
        MAX_CONCRETE_STRAIN,
        "",
        "Concrete strain at f'c",
        "ACI 318-19 22.2.2.1",
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

    cover_to_center = cover_type == "Center"
    spiral_reinf = transverse_type == "Spiral"

    column = Column(
        w,
        h,
        bar_size,
        bar_cover,
        bars_x,
        bars_y,
        fc,
        fy,
        cover_to_center,
        spiral_reinf,
        A_b,
        E_s,
        e_c,
    )

    full_calc(column, load_combos)
