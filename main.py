from efficalc import (
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
)
from efficalc.report_builder import CalculationReportBuilder
from examples.simple.concrete_beam_neutral_axis import calculation as test_calc


def calculation():
    Title("Test Visual Representations")
    Assumption("Lightweight concrete is used.")
    Assumption("All foundations lie above the frost line.")
    Assumption("Loads applied after concrete reaches 28 day strength.")

    Heading("Heading Number 1.")
    Heading("Heading Number 2.", 0)
    Heading("Heading Number 2.1.", 2)
    Heading("Heading Number 2.2.", 2)
    Heading("Heading Number 2.2.1.", 3)
    Heading("Heading Number 2.2.1.1.", 4)
    Heading("Heading Number 2.3.", 2)
    Heading("Heading Number 2.3.1.", 3)
    Heading("Heading Number 3.", 1)
    Heading("Heading Number 4.", 1)
    Heading("Heading Number 5.", 1)
    Heading("Heading Number 5.1.1.1.", 4)

    a = Input("a^2_v", 5, "in", reference="AISC 7-16")
    b = Input("b_{var}", 0.2, "in^2")
    e = Input("Es", 29000, "ksi", "An input with a description.")
    f = Input(
        "F_y",
        50,
        "ksi",
        "Description plus a code reference for the input.",
        reference="AISC Eq. F.2.2",
    )

    num = Calculation("num", a, "in", "A constant calculation.", "AISC ref1")
    short = Calculation(
        "c", a * b, "in^2", description="This is the product", result_check=True
    )
    long = Calculation(
        "long",
        a - e + brackets(b * a * e) + b - e - a - b,
        "mm^2",
        "A long calculation should still display well",
        "ASCE 7-16 Ch.8",
    )

    Comparison(
        a, ">=", b, "Good", "Bad", "Checking that the comparison is all good", "ACI 318"
    )
    Comparison(
        e,
        "<=",
        f,
        "Good",
        "Bad",
        "Checking that the comparison is NO GOOD",
    )

    TextBlock("This is some text before we show a comparison statement that num=b.")
    ComparisonStatement(num, "=", b, reference="any ref 123")

    TextBlock(
        "Now we'll show that short is not long but long is greater than a",
        reference="idk",
    )
    ComparisonStatement(short, "!=", long, ">", a)


if __name__ == "__main__":
    # builder = CalculationReportBuilder(test_calc)
    builder = CalculationReportBuilder(calculation)
    builder.view_report()
