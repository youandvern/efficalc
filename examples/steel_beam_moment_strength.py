from efficalc import (
    PI,
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    Symbolic,
    TextBlock,
    Title,
    brackets,
    ft_to_in,
    minimum,
    sqrt,
)
from efficalc.sections import get_aisc_wide_flange


def calculation(chosen_section_name: str = None):
    Title("Steel Beam Moment Strength")

    TextBlock("Flexural design strength of a steel wide-flange beam section.")

    Heading("Assumptions", numbered=False)
    Assumption("AISC 14th Edition controls design")
    Assumption("Beam web is unstiffened")
    Assumption("Beam design is not controlled by deflection requirements")

    Heading("Inputs", numbered=False)

    Mu = Input("M_u", 30, "kip-ft", "Beam ultimate moment demand")
    Lbu = Input("L_b", 20, "ft", "Beam unbraced length")

    # Select a section size if one isn't provided as an input to the function
    section = (
        Input(
            "section",
            "W18X40",
            description="Beam section size",
            input_type="select",
            select_options=EFFICIENT_AISC_WIDE_FLANGE_BEAM_NAMES,
        )
        if chosen_section_name is None
        else None
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

    # If a section size is provided as an input to the function, use that. Otherwise, use the section size selected
    # using the input object.
    Heading("Section Properties", numbered=False)
    if chosen_section_name:
        Symbolic("section", chosen_section_name, result_check=True)
    else:
        chosen_section_name = section.get_value()

    chosen_section_props = get_aisc_wide_flange(chosen_section_name)
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
        (1.95 * rts / ft_to_in * Es / (0.7 * Fy))
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

    return {"design_strength": PMn.result(), "demand": Mu.get_value()}


# These are the W-Shapes Selection by Zx (AISC 14th edition Table 3-2)
EFFICIENT_AISC_WIDE_FLANGE_BEAM_NAMES = [
    "W40X167",
    "W40X149",
    "W36X160",
    "W36X135",
    "W33X141",
    "W33X130",
    "W33X118",
    "W30X116",
    "W30X108",
    "W30X99",
    "W30X90",
    "W27X84",
    "W24X84",
    "W24X76",
    "W24X68",
    "W24X62",
    "W24X55",
    "W21X68",
    "W21X62",
    "W21X55",
    "W21X50",
    "W21X48",
    "W21X44",
    "W18X55",
    "W18X40",
    "W18X35",
    "W16X40",
    "W16X31",
    "W16X26",
    "W14X34",
    "W14X30",
    "W14X26",
    "W14X22",
    "W12X26",
    "W12X22",
    "W12X19",
    "W12X16",
    "W12X14",
    "W10X22",
    "W10X19",
    "W10X12",
    "W8X10",
]
