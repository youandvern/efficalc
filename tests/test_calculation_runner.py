import pytest

from efficalc import (
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    TextBlock,
    Title,
    clear_saved_objects,
    get_all_calc_objects,
    get_override_or_default_value,
)
from efficalc.calculation_runner import CalculationRunner


@pytest.fixture
def calc_function():
    def calc():
        Title("First thing")
        Assumption("Assume one thing")
        Assumption("Another assumption")
        a = Input("in_{put}", 4, "in")
        Calculation("cal^c", a**2, "in^2")
        Calculation("calc-result", a + 1, result_check=True)
        Comparison(2, ">", a, result_check=False)
        Comparison(a, "<", 5)
        ComparisonStatement(1, "<", a, "<", 12)
        Heading("Section 1")
        TextBlock("Some description")

    yield calc  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


def test_order_of_objects_and_duplicate_types_maintained(calc_function):
    runner = CalculationRunner(calc_function)
    [o_0, o_1, o_2, o_3, o_4, o_5, o_6, o_7, o_8, o_9, o_10] = (
        runner.calculate_all_items()
    )
    assert isinstance(o_0, Title) and o_0.text == "First thing"
    assert isinstance(o_1, Assumption) and o_1.text == "Assume one thing"
    assert isinstance(o_2, Assumption) and o_2.text == "Another assumption"
    assert isinstance(o_3, Input) and o_3.name == "in_{put}"
    assert isinstance(o_4, Calculation) and o_4.result() == 16
    assert isinstance(o_5, Calculation) and o_5.result() == 5
    assert isinstance(o_6, Comparison) and o_6.a == 2
    assert isinstance(o_7, Comparison) and o_7.a == o_3
    assert isinstance(o_8, ComparisonStatement) and o_8.c == 12
    assert isinstance(o_9, Heading) and o_9.text == "Section 1"
    assert isinstance(o_10, TextBlock) and o_10.text == "Some description"


def test_runner_keeps_global_storage_clean_after_run(calc_function):
    runner = CalculationRunner(calc_function, {"in_{put}": 1})
    runner.calculate_all_items()
    assert len(get_all_calc_objects()) == 0
    assert get_override_or_default_value("in_{put}", 3.2) == 3.2
    runner.calculate_results()
    assert get_override_or_default_value("in_{put}", 3.2) == 3.2
    assert len(get_all_calc_objects()) == 0


def test_input_uses_default_value_when_no_override(calc_function):
    runner = CalculationRunner(calc_function)
    all_obj = runner.calculate_all_items()
    input_obj = all_obj[3]
    assert isinstance(input_obj, Input)
    assert input_obj.get_value() == 4
    calc_obj = all_obj[4]
    assert isinstance(calc_obj, Calculation)
    assert calc_obj.result() == 16


def test_input_uses_override_value_when_present(calc_function):
    runner = CalculationRunner(calc_function, {"in_{put}": 3.2})
    all_obj = runner.calculate_all_items()
    input_obj = all_obj[3]
    assert isinstance(input_obj, Input)
    assert input_obj.get_value() == 3.2
    calc_obj = all_obj[4]
    assert isinstance(calc_obj, Calculation)
    assert calc_obj.result() == pytest.approx(10.24)


def test_calculate_results_only_returns_result_checks(calc_function):
    runner = CalculationRunner(calc_function)
    results = runner.calculate_results()
    assert len(results) == 2
    [calc, comparison] = results
    assert isinstance(calc, Calculation)
    assert calc.name == "calc-result"
    assert isinstance(comparison, Comparison)
    assert comparison.b == 5
