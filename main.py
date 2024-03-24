"""
This module provides a sample usage for the efficalc package with a calculation for visually testing the package.
"""

from efficalc import (
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    FigureFromFile,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
)
from efficalc.report_builder import ReportBuilder
from efficalc.sections import get_aisc_wide_flange
from examples.simple.concrete_beam_neutral_axis import calculation as example_calc


def calculation():
    FigureFromFile(r".\docs_src\efficalc.png")

    Title("Welcome to efficalc calculations")

    Assumption('You\'ve read the "Quickstart" guide in the project README.')
    Assumption("You've seen that we have a full documentation site.")
    Assumption("You want to make better calculations")

    Heading("Inputs")

    a = Input(
        "a^2_v",
        5,
        description="Names with sub and superscripts",
    )
    b = Input(
        "b_{var}",
        0.2,
        "in^2",
        "Units can also have sub and superscripts",
    )
    f = Input(
        "F_y",
        50,
        "ksi",
        "This input includes a code reference",
        reference="AISC Eq. F.2.2",
    )

    section_name = Input(
        "WF \ Section \ Name",
        "W18X40",
        description="Choose beam section size as your input, get the section properties below",
    )

    Heading("Section Properties")
    TextBlock("These are automatically fetched from our shapes database.")
    chosen_section_props = get_aisc_wide_flange(section_name.get_value())
    Sx = Calculation("S_x", chosen_section_props.Sx, "in^3")
    Zx = Calculation("Z_x", chosen_section_props.Zx, "in^3")
    ry = Calculation("r_{y}", chosen_section_props.ry, "in")

    Heading("Calculations")

    num = Calculation(
        "num", a, "in", 'A "calculated" constant with a code reference', "AISC ref1"
    )
    short = Calculation(
        "c", a * b, "in^2", description="This is a product", result_check=True
    )
    long = Calculation(
        "long",
        a - f + brackets(b * a * f) + b - Sx - Zx - b,
        "mm^2",
        "A long calculation should still display well",
        "ASCE 7-16 Ch.8",
    )

    Heading("Comparisons (Design Checks)")

    Comparison(
        a,
        ">=",
        b,
        "Good",
        "Bad",
        "Compare two variables as a design check indicator",
        "ACI 318",
    )

    Comparison(
        f,
        "<=",
        ry,
        "Good",
        "Bad",
        "Checking that the comparison is not true (BAD)",
    )

    TextBlock("This is some text before we show a comparison statement that num=b.")
    ComparisonStatement(num, "=", b, reference="any ref 123")

    TextBlock(
        "Now we'll show that short is not long but long is greater than a. Even text blocks can have references.",
        reference="idk",
    )
    ComparisonStatement(short, "!=", long, ">", a)


if __name__ == "__main__":
    # builder = ReportBuilder(example_calc)
    builder = ReportBuilder(calculation)
    builder.view_report()
