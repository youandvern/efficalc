from efficalc import (
    Calculation,
    Comparison,
    Heading,
    Input,
    TextBlock,
    Title,
    Symbolic,
    r_brackets,
)
import try_axis


def calculation(col):
    Heading("Inputs")

    w = Input("w", col.w, "in", description="Column section width (x dimension)")
    h = Input("h", col.h, "in", description="Column section height (y dimension)")
    Input("", "\\" + col.bar_size, "", description="Rebar size")
    bar_area = Input(
        "A_{\\mathrm{bar}}", col.bar_area, "in^2", description="Area of one bar"
    )
    transverse_type = "Spiral" if col.spiral_reinf else "Tied"
    Input("", transverse_type, "", description="Transverse reinforcement type")
    bars_x = Input(
        "\mathrm{n_{bars,\ x}}",
        col.bars_x,
        "",
        description="Number of bars on the top/bottom edges",
    )
    bars_y = Input(
        "\mathrm{n_{bars,\ y}}",
        col.bars_y,
        "",
        description="Number of bars on the left/right edges",
    )
    fc = Input("f'_c", col.fc / 1000, "ksi", description="Concrete strength")
    fy = Input("f_y", col.fy, "ksi", description="Steel strength")

    steel_area = Calculation(
        "A_{st}",
        bar_area * r_brackets(2 * bars_x + 2 * bars_y - 4),
        "in^2",
        "Total area of longitudinal reinforcement",
    )
    tot_area = Calculation("A_g", w * h, "in^2", "Gross section area")
    max_pn = Calculation(
        "P_0",
        0.85 * fc * r_brackets(tot_area - steel_area) + fy * steel_area,
        "kips",
        "Compressive capacity",
        "ACI 318-19 22.4.2.2",
    )
    if col.spiral_reinf:
        TextBlock("Because the transverse reinforcement is spiral:")
        max_pn_limit = Calculation(
            "P_{\mathrm{n,max}}",
            0.85 * max_pn,
            "kips",
            "Maximum axial strength",
            "ACI 318-19 22.4.2.1(b)",
        )
        phi = Calculation(
            "\\phi",
            0.75,
            "",
            "",
            "ACI 318-19 Table 21.2.2(a)",
        )
    else:
        TextBlock("Because the transverse reinforcement is tied:")
        max_pn_limit = Calculation(
            "P_{\mathrm{n,max}}",
            0.80 * max_pn,
            "kips",
            "Maximum axial strength",
            "ACI 318-19 22.4.2.1(a)",
        )
        phi = Calculation(
            "\\phi",
            0.65,
            "",
            "",
            "ACI 318-19 Table 21.2.2(b)",
        )

    max_phi_pn = Calculation("{\\phi}P_{\mathrm{n,max}}", phi * max_pn_limit, "kips")

    min_pn = Calculation(
        "P_{\mathrm{nt,max}}",
        fy * steel_area,
        "kips",
        "Tensile capacity",
        "ACI 318-19 22.4.3.1",
    )

    phi = Calculation(
        "\\phi",
        try_axis.PHI_FLEXURE,
        "",
        "Because failure is tension-controlled:",
        "ACI 318-19 21.2.2(e)",
    )
    min_phi_pn = Calculation("{\\phi}P_{\mathrm{nt,max}}", phi * min_pn, "kips")
    return (
        max_pn.get_value(),
        max_phi_pn.get_value(),
        -min_pn.get_value(),
        -min_phi_pn.get_value(),
    )
