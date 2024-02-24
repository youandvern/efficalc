from efficalc import Heading
from efficalc.base_definitions.assumption import Assumption
from efficalc.base_definitions.calculation import Calculation
from efficalc.base_definitions.input import Input
from efficalc.base_definitions.title import Title
from efficalc.report_builder import CalculationReportBuilder


def test_calc():
    Title("Example Calculation")
    Assumption(
        "Use a good code document with really great calculations so that you get accurate results and the building doesn't fall down. That's super important for the best calculations."
    )

    Heading("Test 1.")
    Heading("Test 2.", 0)
    Heading("Test 2.1.", 2)
    Heading("Test 2.2.", 2)
    Heading("Test 2.2.1.", 3)
    Heading("Test 2.2.1.1.", 4)
    Heading("Test 2.3.", 2)
    Heading("Test 2.3.1.", 3)
    Heading("Test 3.", 1)
    Heading("Test 4.", 1)
    Heading("Test 5.", 1)
    Heading("Test 5.1.1.1.", 4)

    a = Input("a^2_v", 5, "in", reference="AISC 7-16")
    b = Input("b_{var}", 0.2, "in^2")

    Calculation(
        "c", a * b, "in^2", description="This is the product", result_check=True
    )


if __name__ == "__main__":
    builder = CalculationReportBuilder(test_calc)
    builder.generate_report()
