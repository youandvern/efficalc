from efficalc import Calculation, Heading, TextBlock, r_brackets
from examples.conc_col_pmm.col.axial_limits import AxialLimits
from examples.conc_col_pmm.col.column import Column
from examples.conc_col_pmm.struct_analysis import try_axis


def calculate_axial_load_limits(col: Column) -> AxialLimits:

    w = col.w_input
    h = col.h_input
    bar_area = col.rebar_area_input
    bars_x = col.bars_x_input
    bars_y = col.bars_y_input
    fc = col.fc_input
    fy = col.fy_input

    Heading("Axial Capacity Calculations")

    steel_area = Calculation(
        "A_{st}",
        bar_area * r_brackets(2 * bars_x + 2 * bars_y - 4),
        "in^2",
        "Total area of longitudinal reinforcement:",
    )
    tot_area = Calculation("A_g", w * h, "in^2", "Gross section area")
    Heading("Compressive Capacity", 2)
    max_pn = Calculation(
        "P_0",
        0.85 * fc / 1000 * r_brackets(tot_area - steel_area) + fy * steel_area,
        "kips",
        "",
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
            "",
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

    Heading("Tensile Capacity", 2)
    min_pn = Calculation(
        "P_{\mathrm{nt,max}}",
        fy * steel_area,
        "kips",
        "",
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

    return AxialLimits(
        max_pn.result(),
        max_phi_pn.result(),
        max_phi_pn,
        -min_pn.result(),
        -min_phi_pn.result(),
    )
