from latexexpr_efficalc import Variable

from efficalc import (
    PI,
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
    ft_to_in,
    maximum,
    minimum,
    sqrt,
)
from efficalc.sections import ALL_AISC_RECTANGULAR_NAMES, get_aisc_rectangular


def calculation():
    Title("Rectangular HSS Compression Design")

    Assumption("Members are in pure compression")
    Assumption("AISC manual of steel (14th ed.) controls member design")
    Assumption("Torsional unbraced length does not exceed lateral unbraced length")

    Heading("Inputs")
    Pu = Input("P_u", 10, "kips", "Ultimate compressive load")

    L = Input("L", 4, "ft", "Member length")
    Kc = Input("k_{c}", 1, "", "Member effective length factor")

    size = Input(
        "Shape",
        "HSS6X2X1/8",
        "",
        "Member section size",
        input_type="select",
        select_options=ALL_AISC_RECTANGULAR_NAMES,
    )

    Fy = Input("F_{y}", 36, "ksi", "Material yield stress")
    Es = Input("E", 29000, "ksi", "Modulus of elasticity")

    Pc = Input("\phi_c", 0.9, "", "Resistance factor for compression")

    Heading("Section Properties")
    section = get_aisc_rectangular(size.get_value())
    Ag = Calculation("A_{g}", section.A, "in^2")
    b = Calculation("b", section.bin, "in")
    h = Calculation("h", section.h, "in")
    tdes = Calculation("t_{des}", section.tdes, "in")
    rx = Calculation("r_x", section.rx, "in")
    ry = Calculation("r_y", section.ry, "in")
    b_t = Calculation("\mathrm{b/t}", section.b_tdes, "")
    h_t = Calculation("\mathrm{h/t}", section.h_tdes, "")

    Heading("Buckling Properties")
    yr = Calculation(
        "\lambda_{r}",
        1.40 * sqrt(Es / Fy),
        "",
        "Element compression slenderness limit",
        reference="AISC Table B4.1a",
    )

    y_max = Calculation(
        "\lambda_{max}", maximum(b_t, h_t), "", "Maximum element slenderness ratio"
    )

    KLr = Calculation(
        "\mathrm{KL/r}",
        Kc * L * ft_to_in / minimum(rx, ry),
        "",
        "Member slenderness ratio",
    )

    Heading(
        "Compressive Strength", head_level=1
    )  # ###############################################
    Fe = Calculation(
        "F_e", PI**2 * Es / KLr**2, "ksi", "Elastic buckling stress", "AISC Eq. E3-4"
    )

    Comparison(
        y_max,
        "<",
        yr,
        true_message="Non-Slender",
        false_message="Slender",
        result_check=False,
    )

    # Non-slender section
    if y_max.result() < yr.result():
        y_crit = Calculation(
            "\lambda_{crit}", 4.71 * sqrt(Es / Fy), "", reference="AISC Section E3"
        )
        if KLr.result() <= y_crit.result():
            ComparisonStatement(KLr, "<=", y_crit)
            TextBlock("...Inelastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                Fy * 0.658 ** (Fy / Fe),
                "ksi",
                "Critical compressive stress",
                "AISC Eq. E3-2",
            )
        else:
            ComparisonStatement(KLr, ">", y_crit)
            TextBlock("...Elastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                0.877 * Fe,
                "ksi",
                "Critical compressive stress",
                "AISC Eq. E3-3",
            )

        Pn = Calculation(
            "P_n",
            Fcr * Ag,
            "kips",
            "Nominal member compressive strength",
            "AISC Eq. E3-1",
        )

    # Slender section
    else:
        EWC = Variable("0.38", 0.38)  # Effective width constant
        Heading(
            "Reduced Effective Widths of Slender Elements (AISC Eq. E7-18)",
            head_level=2,
        )
        if b_t.result() > yr.result():
            ComparisonStatement(b_t, ">", yr)
            TextBlock("Side B is slender.")
            be = Calculation(
                "b_e",
                1.92 * tdes * sqrt(Es / Fy) * brackets(1 - EWC / b_t * sqrt(Es / Fy)),
                "in",
            )
        else:
            ComparisonStatement(b_t, "<", yr)
            TextBlock("Side B is not slender.")
            be = Calculation(
                "b_e",
                b,
                "in",
            )

        if h_t.result() > yr.result():
            ComparisonStatement(h_t, ">", yr)
            TextBlock("Side Ht is slender.")
            he = Calculation(
                "h_e",
                1.92 * tdes * sqrt(Es / Fy) * brackets(1 - EWC / h_t * sqrt(Es / Fy)),
            )
        else:
            ComparisonStatement(h_t, "<", yr)
            TextBlock("Side Ht is not slender.")
            he = Calculation(
                "h_e",
                h,
                "in",
            )

        bi = Calculation(
            "b_i", maximum(0, b - be), "in", "Ineffective length on side B"
        )
        hi = Calculation(
            "h_i", maximum(0, h - he), "in", "Ineffective length on side Ht"
        )

        Heading(
            "Reduction Factor for Slender Stiffened Elements (AISC Section E7.2)",
            head_level=2,
        )
        Ae = Calculation(
            "A_e",
            Ag - bi * tdes * 2 - hi * tdes * 2,
            "in^2",
            "Effective cross-sectional area",
        )
        Qa = Calculation(
            "Q_a",
            Ae / Ag,
            "",
            "Reduction factor for cross-section",
            reference="AISC Eq. E7-16",
        )

        Heading("Nominal Compressive Strength (AISC Section E7)", head_level=2)

        y_crit = Calculation("\lambda_{crit}", 4.71 * sqrt(Es / (Qa * Fy)), "")
        if KLr.result() <= y_crit.result():
            ComparisonStatement(KLr, "<=", y_crit)
            TextBlock("...Inelastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                Qa * Fy * 0.658 ** (Qa * Fy / Fe),
                "ksi",
                "Critical compressive stress",
                "AISC Eq. E7-2",
            )
        else:
            ComparisonStatement(KLr, ">", y_crit)
            TextBlock("...Elastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                0.877 * Fe,
                "ksi",
                "Critical compressive stress",
                "AISC Eq. E7-3",
            )

        Pn = Calculation(
            "P_n",
            Fcr * Ag,
            "kips",
            "Nominal member compressive strength",
            "AISC Eq. E7-1",
        )

    Heading("Member Demand vs. Capacity Check", head_level=1)
    PPn = Calculation(
        "\phi P_n",
        Pc * Pn,
        "kips",
        "Design member compressive capacity",
        result_check=True,
    )
    Comparison(
        Pu, "<=", PPn, true_message="OK", false_message="ERROR", result_check=True
    )
