from efficalc import (
    Calculation,
    Comparison,
    Heading,
    Input,
    TextBlock,
    Title,
    r_brackets,
    ComparisonStatement,
    Assumption,
    cos,
    sin,
    tan,
    minimum,
    maximum,
    PI,
    sqrt,
    Table,
)
import math
import random
import sections


def calculation(
    col=sections.Column(20, 30, "#8", 1.5, 3, 5, 8000, 60, False, False),
    theta_input=0,
    c_input=10,
):

    Title("Concrete Column Biaxial Bending")
    TextBlock(
        "Determine axial and moment capacity of a symmetrically-reinforced rectangular concrete column subject to "
        + "bending on a given neutral axis angle and depth."
    )

    Assumption("ACI 318-19 controls the design")
    Assumption("Reinforcement is non-prestressed")
    Assumption(
        "Lap splices of longitudinal reinforcement are in accordance with ACI 318-19 Table 10.7.5.2.2"
    )
    Assumption(
        "Strain in concrete and reinforcement is proportional to distance from the neutral axis, per ACI 318-19 22.2.1.2 "
    )

    Heading("Inputs")
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
    theta = Input("\\theta", theta_input, "rad", description="Neutral axis angle")
    c = Input("c", c_input, "in", description="Neutral axis depth")

    STEEL_E = Input(
        "E_s", 29000, "ksi", "Steel modulus of elasticity", "ACI 318-19 20.2.2.2"
    )
    CONC_EPSILON = Input(
        "\\epsilon_u", 0.003, "", "Concrete strain at f'c,", "ACI 318-19 22.2.2.1"
    )

    Heading("Calculations")

    # this function returns the lambda, eccentricity, pn, phi_pn, and phi_mn
    # from particular neutral axis angle and neutral axis depth c. The neutral
    # axis angle must be between -90 degrees and 0 degrees, inclusive, and the
    # neutral axis depth must be greater than or equal to 0

    if c == 0:
        TextBlock(
            "Because the neutral axis depth is zero, the column is in pure tension."
        )
        return
    TextBlock(
        "Define variables for summing the contributions to the axial and moment capacities:"
    )
    pn = Calculation("P_{\\mathrm{n, cumulative}}", 0, "kips")
    mnx = Calculation("M_{\\mathrm{nx, cumulative}}", 0, "kip-in")
    mny = Calculation("M_{\\mathrm{ny, cumulative}}", 0, "kip-in")

    Heading("Forces in the Concrete", 3)

    if fc.get_value() <= 4000:
        ComparisonStatement(2500, "<=", fc, "<=", 4000)
        beta1 = Calculation(
            "\\beta_1",
            0.85,
            "",
            "",
            "ACI318-19 Table 22.2.2.4.3(a)",
        )
    elif fc.get_value() < 8000:
        ComparisonStatement(4000, "<", fc, "<", 8000)
        beta1 = Calculation(
            "\\beta_1",
            0.85 - 0.05 * r_brackets(fc - 4000) / 1000,
            "",
            "",
            "ACI318-19 Table 22.2.2.4.3(b)",
        )
    else:
        ComparisonStatement(fc, ">=", 8000)
        beta1 = Calculation(
            "\\beta_1",
            0.65,
            "",
            "",
            "ACI318-19 Table 22.2.2.4.3(c)",
        )
    a = Calculation(
        "a",
        beta1 * c,
        "in",
        "Depth of equivalent compression zone",
        "ACI 318-19 22.2.2.4.1",
    )
    fc = Calculation(
        "f'_c", fc / 1000, "ksi", description="Concrete strength converted to ksi:"
    )
    epsilon = 1e-6  # acceptable error for considering the neutral axis to
    # be vertical or horizontal

    intersects = [False] * 4  # whether line of concrete compression intersects the
    # left, top, right, and bottom edges of the section
    if theta.get_value() > -math.pi / 2 + epsilon:
        left_y_temp = (
            col.half_h
            - a.get_value() / math.cos(theta.get_value())
            - col.w * math.tan(theta.get_value())
        )
        intersects[0] = -col.half_h < left_y_temp < col.half_h
        if intersects[0]:
            left_y = Calculation(
                "y_{\\mathrm{left}}",
                h / 2 - a / cos(theta) - w * tan(theta),
                "in",
                " y coordinate of equivalent compression zone intersection with left edge:",
            )

        right_y = col.half_h - a.get_value() / math.cos(theta.get_value())
        intersects[2] = -col.half_h < right_y < col.half_h
        if intersects[2]:
            right_y = Calculation(
                "y_{\\mathrm{right}}",
                h / 2 - a / cos(theta),
                "in",
                " y coordinate of equivalent compression zone intersection with right edge:",
            )

    if theta.get_value() < -epsilon:
        top_x_temp = col.half_w + a.get_value() / math.sin(theta.get_value())
        intersects[1] = -col.half_w < top_x_temp < col.half_w
        if intersects[1]:
            top_x = Calculation(
                "x_{\\mathrm{top}}",
                w / 2 + a / sin(theta),
                "in",
                " x coordinate of equivalent compression zone intersection with top edge:",
            )

        # if theta is -90, take the tan of 0 and get a change
        # of zero, and if theta is -45, take the tan of 45
        # and get somewhat of an increase in x
        bot_x_temp = (
            col.half_w
            + a.get_value() / math.sin(theta.get_value())
            + col.h * math.tan(PI / 2 + theta.get_value())
        )
        intersects[3] = -col.half_w < bot_x_temp < col.half_w
        if intersects[3]:
            bot_x = Calculation(
                "x_{\\mathrm{bottom}}",
                w / 2 + a / cos(theta) + h * tan(theta),
                "in",
                " x coordinate of equivalent compression zone intersection with bottom edge:",
            )

    if not any(intersects):  # the whole concrete section is in compression
        pn = Calculation("P_{\\mathrm{n, cumulative}}", 0.85 * fc * w * h, "kips")
    else:

        def add_axial_moment(pt_a, pt_b, pt_c):
            nonlocal pn, mnx, mny
            tri_area = Calculation(
                "A_{\\mathrm{triangle}}",
                0.5
                * abs(
                    pt_a[0] * pt_b[1]
                    + pt_b[0] * pt_c[1]
                    + pt_c[0] * pt_a[1]
                    - pt_a[0] * pt_c[1]
                    - pt_b[0] * pt_a[1]
                    - pt_c[0] * pt_b[1]
                ),
                "in^2",
                "Calculate the area of this triangular compression zone:",
            )
            pn = Calculation(
                "P_{\\mathrm{n, cumulative}}", pn + 0.85 * fc * tri_area, "kips"
            )
            centr_x = Calculation(
                "x_{\\mathrm{centroid}}",
                (pt_a[0] + pt_b[0] + pt_c[0]) / 3,
                "in",
                "x coordinate of the centroid of this zone:",
            )
            centr_y = Calculation(
                "y_{\\mathrm{centroid}}",
                (pt_a[1] + pt_b[1] + pt_c[1]) / 3,
                "in",
                "y coordinate of the centroid of this zone:",
            )
            mnx = Calculation(
                "M_{\\mathrm{nx, cumulative}}",
                mnx + 0.85 * fc * tri_area * centr_y,
                "kip-in",
            )
            mny = Calculation(
                "M_{\\mathrm{ny, cumulative}}",
                mny + 0.85 * fc * tri_area * centr_x,
                "kip-in",
            )

        pt1 = (-w / 2, left_y) if intersects[0] else (top_x, h / 2)
        pt2 = (bot_x, -h / 2) if intersects[3] else (w / 2, right_y)

        add_axial_moment(pt1, pt2, (w / 2, h / 2))  # compression triangle to
        # top right corner
        if intersects[0]:  # there is a compression triangle to top left corner
            add_axial_moment((-w / 2, h / 2), (w / 2, h / 2), pt1)
        if intersects[3]:  # there is a compression triangle to bot right corner
            add_axial_moment((w / 2, -h / 1), (w / 2, h / 2), pt2)

    def add_bar(coords):
        nonlocal pn, mnx, mny
        bar_calc = coords.copy()
        # "offset" is the distance from the center of the bar to the line
        # passing through the top right corner of the section and parallel to
        # the neutral axis
        offset = (col.w / 2 - coords[0]) * math.cos(theta.get_value() + math.pi / 2) + (
            col.h / 2 - coords[1]
        ) * math.sin(theta.get_value() + math.pi / 2)
        bar_calc.append(round(offset, 2))
        strain = CONC_EPSILON.get_value() * (offset - c.get_value()) / c.get_value()
        bar_calc.append(round(strain, 1))
        stress = min(
            fy.get_value(),
            max(
                -fy.get_value(),
                CONC_EPSILON.get_value()
                * STEEL_E.get_value()
                * (offset - c.get_value())
                / c.get_value(),
            ),
        )
        bar_calc.append(round(stress, 1))
        in_comp_zone = offset < a.get_value()
        if in_comp_zone:
            stress += 0.85 * fc.get_value()
            bar_calc.append(round(0.85 * fc.get_value(), 1))
        else:
            bar_calc.append(0)
        # since negative strain and negative stress are defined as
        # compression for rebar but compression is positive in the conc.
        # the sign of everything needs to be changed
        pn -= bar_area.get_value() * stress
        bar_calc.append(round(-bar_area.get_value() * stress, 1))
        mnx -= bar_area.get_value() * stress * coords[1]
        bar_calc.append(round(-bar_area.get_value() * stress * coords[1], 1))
        mny -= bar_area.get_value() * stress * coords[0]
        bar_calc.append(round(-bar_area.get_value() * stress * coords[0], 1))

        rebar_matrix.append(bar_calc)

    Heading("Forces in the Rebar", 3)
    right_bar_x = col.half_w - col.edge_to_bar_center  # x coordinate of bars on the
    # right edge
    y = col.y_start
    # iterate over the bars along the left and right lines
    # (this includes corner bars)
    bar_count = 0

    headers = [
        "X Coordinate (in)",
        "Y Coordinate (in)",
        "Effective Depth d (in)",
        "Strain (unitless)",
        "Stress (ksi)",
        "Stress Correction for Displaced Concrete (ksi)",
        "Axial Force (kips)",
        "Contribution to M_x (kip-in)",
        "Contribution to M_y (kip-in)",
    ]
    rebar_matrix = []
    for i in range(col.bars_y):
        for x in (-right_bar_x, right_bar_x):
            coords = [x, y]
            bar_count += 1
            add_bar(coords)
        y += col.y_space

    top_bar_y = col.half_h - col.edge_to_bar_center  # y coordinate of bars on the
    # top edge
    x = col.x_start
    for i in range(col.bars_x - 2):
        # iterate over the bars along the top and bottom lines, and add the
        # force for each one
        for y in (-top_bar_y, top_bar_y):
            coords = [x, y]
            add_bar(coords)
        x += col.x_space
    Table(rebar_matrix, headers, "Rebar Calculations")

    Heading("Capacity Calculations", 3)
    lambda1 = math.atan2(mny, mnx)  # atan2 takes y,x, and we want mny at top

    # if Mx and My are both zero, the angle isn't defined, so return a random
    # number to help avoid divide by zero errors
    if not (mnx or mny):
        lambda1 = random.uniform(0, math.pi / 2)

    TextBlock("The extreme tension reinforcement is centered at these coordinates:")
    coords = [0, 0]
    coords[0] = Input("x_{\\mathrm{bar}}", -right_bar_x, "in")
    coords[1] = Input("y_{\\mathrm{bar}}", -top_bar_y, "in")
    offset = Calculation(
        "d_t",
        r_brackets(w / 2 - coords[0]) * cos(theta + PI / 2)
        + r_brackets(h / 2 - coords[1]) * sin(theta + PI / 2),
        "in",
    )
    max_strain = Calculation(
        "\\epsilon_y", CONC_EPSILON * r_brackets(offset - c) / c, ""
    )
    yield_strain = Calculation("\\epsilon_{ty}", fy / STEEL_E, "")
    if max_strain.get_value() <= yield_strain.get_value():
        Comparison(max_strain, "<=", yield_strain)
        strain_level = 0
    elif (
        yield_strain.get_value()
        < max_strain.get_value()
        < yield_strain.get_value() + 0.003
    ):
        Comparison(yield_strain, "<", max_strain, "<", yield_strain + 0.003)
        strain_level = 1
    else:
        Comparison(max_strain, ">=", yield_strain + 0.003)
        strain_level = 2
    if col.spiral_reinf:
        if strain_level == 0:
            phi = Calculation(
                "\\phi",
                0.75,
                "",
                "Failure is compression-controlled and transverse reinforcement is spiral:",
                "ACI 318-19 Table 21.2.2(a)",
            )
        elif strain_level == 1:
            phi = Calculation(
                "\\phi",
                0.75 + 0.15 * r_brackets(max_strain - yield_strain) / 0.003,
                "",
                "Failure is transition and transverse reinforcement is spiral:",
                "ACI 318-19 Table 21.2.2(c)",
            )
        else:
            phi = Calculation(
                "\\phi",
                0.90,
                "",
                "Failure is tension-controlled and transverse reinforcement is spiral:",
                "ACI 318-19 Table 21.2.2(e)",
            )
    else:
        if strain_level == 0:
            phi = Calculation(
                "\\phi",
                0.65,
                "",
                "Failure is compression-controlled and transverse reinforcement is tied:",
                "ACI 318-19 Table 21.2.2(b)",
            )
        elif strain_level == 1:
            phi = Calculation(
                "\\phi",
                0.65 + 0.25 * r_brackets(max_strain - yield_strain) / 0.003,
                "",
                "Failure is transition and transverse reinforcement is tied:",
                "ACI 318-19 Table 21.2.2(d)",
            )
        else:
            phi = Calculation(
                "\\phi",
                0.90,
                "",
                "Failure is tension-controlled and transverse reinforcement is tied:",
                "ACI 318-19 Table 21.2.2(f)",
            )
    TextBlock("Factored axial and moment capacities:")
    phi_pn = Calculation("{\\phi}P_n", phi * pn, "kips")
    phi_mnx = Calculation("{\\phi}M_{nx}", phi * mnx / 12, "kip-ft")
    phi_mny = Calculation("{\\phi}M_{nx}", phi * mny / 12, "kip-ft")

    phi_mn_xy = Calculation("{\\phi}M_{nxy}", sqrt(phi_mnx**2 + phi_mny**2), "kip-ft")
