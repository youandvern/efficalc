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
    minimum,
    sqrt,
)
from efficalc.sections import ALL_AISC_WIDE_FLANGE_NAMES, get_aisc_wide_flange


def calculation():
    Title("Steel Beam Moment Strength")

    TextBlock("Flexural strength of a steel wide-flange beam section.")

    Heading("Assumptions", numbered=False)
    Assumption("AISC 14th Edition controls design")
    Assumption("Beam web is unstiffened")

    Heading("Inputs", numbered=False)

    Mu = Input("M_u", 30, "kip-ft", "Beam ultimate moment demand")
    Lbu = Input("L_b", 20, "ft", "Beam unbraced length")

    section = Input(
        "section",
        "W18X40",
        description="Beam section size",
        input_type="select",
        select_options=ALL_AISC_WIDE_FLANGE_NAMES[150:200],
    )

    Fy = Input("F_y", 50, "ksi", "Steel yield strength")
    Es = Input("E", 29000, "ksi", "Modulus of elasticity")

    Cb = Input(
        "C_b",
        1.0,
        "",
        "Lateral-torsional buckling modification factor",
        reference="AISC F1(3)",
    )

    Heading("Section Properties", numbered=False)
    chosen_section_props = get_aisc_wide_flange(section.get_value())
    Sx = Calculation("S_x", chosen_section_props.Sx, "in^3")
    Zx = Calculation("Z_x", chosen_section_props.Zx, "in^3")
    ry = Calculation("r_{y}", chosen_section_props.ry, "in")
    rts = Calculation("r_{ts}", chosen_section_props.rts, "in")
    J = Calculation("J", chosen_section_props.J, "in^4")
    ho = Calculation("h_o", chosen_section_props.ho, "in")
    bf_2tf = Calculation("b_f/2t_f", chosen_section_props.bf_2tf, "")
    h_tw = Calculation("h/t_w", chosen_section_props.h_tw, "")

    Heading("Beam Flexural Capacity", head_level=1)
    Pb = Calculation(
        r"\phi_{b}", 0.9, "", "Flexural resistance factor", reference="AISC F1(1)"
    )

    Heading("Section Compactness", head_level=2)
    ypf = Calculation(
        r"\lambda_{pf}", 0.38 * sqrt(Es / Fy), "", reference="AISC Table B4.1b(10)"
    )
    Comparison(
        bf_2tf,
        "<=",
        ypf,
        true_message="CompactFlange",
        false_message="ERROR:NotCompactFlange",
        result_check=False,
    )

    ypw = Calculation(
        r"\lambda_{pw}", 3.76 * sqrt(Es / Fy), "", reference="AISC Table B4.1b(15)"
    )
    Comparison(
        h_tw,
        "<=",
        ypw,
        true_message="CompactWeb",
        false_message="ERROR:NotCompactWeb",
        result_check=False,
    )

    Heading("Plastic Moment Strength", head_level=2)
    Mp = Calculation(
        "M_{p}",
        Fy * Zx / ft_to_in,
        "kip-ft",
        "Nominal plastic moment strength",
        reference="AISC Eq. F2-1",
    )

    Heading("Yielding Strength", head_level=2)
    Mny = Calculation("M_{ny}", Mp, "kip-ft", reference="AISC Eq. F2-1")

    Heading("Lateral-Torsional Buckling", head_level=2)
    Lp = Calculation(
        "L_{p}", 1.76 * ry * sqrt(Es / Fy) / ft_to_in, "ft", reference="AISC Eq. F2-5"
    )
    cc = Calculation("c", 1.0, "", reference="AISC Eq. F2-8a")
    Lr = Calculation(
        "L_{r}",
        1.95
        * rts
        / ft_to_in
        * Es
        / (0.7 * Fy)
        * sqrt(
            J * cc / (Sx * ho)
            + sqrt((J * cc / (Sx * ho)) ** 2 + 6.76 * (0.7 * Fy / Es) ** 2)
        ),
        "ft",
        reference="AISC Eq. F2-6",
    )

    if Lbu.result() <= Lp.result():
        ComparisonStatement(Lbu, "<=", Lp)
        Mnl = Calculation(
            "M_{nltb}",
            Mp,
            "kip-ft",
            "The limit state of lateral-torsional buckling does not apply",
            reference="AISC F2.2(a)",
        )
    elif Lbu.result() > Lr.result():
        ComparisonStatement(Lbu, ">", Lr)
        Fcr = Calculation(
            "F_{cr}",
            Cb * PI**2 * Es / (Lbu * ft_to_in / rts) ** 2
            + sqrt(1 + 0.078 * J * cc / (Sx * ho) * (Lbu * ft_to_in / rts) ** 2),
            "ksi",
            reference="AISC Eq. F2-4",
        )
        Mncr = Calculation(
            "M_{ncr}", Fcr * Sx / ft_to_in, "kip-ft", reference="AISC F2.2(c)"
        )
        Mnl = Calculation(
            "M_{nltb}", minimum(Mncr, Mp), "kip-ft", reference="AISC Eq. F2-3"
        )
    else:
        ComparisonStatement(Lp, "<", Lbu, "<=", Lr)
        Mncr = Calculation(
            "M_{ncr}",
            Cb
            * brackets(
                Mp - brackets(Mp - 0.7 * Fy * Sx / ft_to_in) * (Lbu - Lp) / (Lr - Lp)
            ),
            "kip-ft",
            reference="AISC F2.2(b)",
        )
        Mnl = Calculation(
            "M_{nltb}", minimum(Mncr, Mp), "kip-ft", reference="AISC Eq. F2-2"
        )

    Heading("Controlling Strength", head_level=2)
    PMn = Calculation(
        r"\phi M_n",
        Pb * minimum(Mny, Mnl),
        "kip-ft",
        "Design flexural strength of the section",
        result_check=True,
    )
    Comparison(Mu, "<=", PMn)
