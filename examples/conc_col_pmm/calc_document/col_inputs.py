from efficalc import (
    Heading,
    Input,
    InputTable,
)

from examples.conc_col_pmm.constants.rebar_data import (
    REBAR_SIZES,
    REBAR_STRENGTHS,
)
from .full_calc_document import calculation as full_calc


# this function accepts inputs from the user and passes them to "full_calc_document"
def calculation():
    Heading("Column Inputs")
    w = Input("w", 20, "in", description="Column section width (x dimension)")
    h = Input("h", 30, "in", description="Column section height (y dimension)")

    # zero spaces
    bar_size = Input(
        "",
        REBAR_SIZES[3],
        "",
        description="Longitudinal rebar size (Imperial)",
        input_type="select",
        select_options=REBAR_SIZES,
    )

    # one space
    bar_cover = Input(" ", 1.5, "in", description="Longitudinal rebar cover")

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
        5,
        "",
        description="Number of bars on the top/bottom edges",
        num_step=1,
    )

    # 5 spaces
    bars_y = Input(
        "     ",
        4,
        "",
        description="Number of bars on the left/right edges",
        num_step=1,
    )
    fc = Input("f'_c", 8000, "psi", description="Concrete strength")

    fy = Input(
        "f_y",
        REBAR_STRENGTHS[1],
        "",
        description="Steel strength",
        input_type="select",
        select_options=REBAR_STRENGTHS,
    )

    headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "Show Calc in Report"]

    default_loads = [[400, -300, 200, True]]
    load_table = InputTable(default_loads, headers, "Load Cases", False, False)

    cover_to_center = cover_type == "Center"
    spiral_reinf = transverse_type == "Spiral"

    col_inputs = [
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
    ]
    full_calc(col_inputs, load_table)
