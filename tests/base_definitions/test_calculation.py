import pytest

from efficalc import (
    Calculation,
    CalculationLength,
    Input,
    clear_all_input_default_overrides,
    get_all_calc_objects,
    reset_results,
    sqrt,
)


@pytest.fixture
def common_setup_teardown():
    data = 5  # Set up a sample number
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    reset_results()


def test_public_members(common_setup_teardown):
    a = Calculation(
        "a", 5, unit="in", description="test desc", reference="a ref", result_check=True
    )
    assert a.name == "a"
    assert a.operation.result() == 5
    assert a.description == "test desc"
    assert a.reference == "a ref"
    assert a.result_check is True
    assert a.error is None
    assert a.unit == "in"


def test_value_constant(common_setup_teardown):
    a = Calculation("a", 5)
    assert a.get_value() == 5
    assert a.result() == 5


def test_value_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Calculation("c", a + b)
    assert c.get_value() == 9
    assert c.result() == 9


def test_result_value_error(common_setup_teardown):
    a = Input("a", -2)
    b = Calculation("b", sqrt(a))
    assert b.error is None
    assert b.result() == 0.0
    assert "could not be calculated" in b.error


def test_result_zero_div_error(common_setup_teardown):
    a = Input("a", -2)
    b = Calculation("b", a / 0.0)
    assert b.error is None
    assert b.result() == 0.0
    assert "could not be calculated" in b.error


def test_expression_with_expressions(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Calculation("c", a + b)
    d = Calculation("d", a - c)
    e = Calculation("e", c * d)
    assert d.get_value() == -7
    assert d.result() == -7
    assert e.get_value() == -63
    assert e.result() == -63


def test_save_calc_item(common_setup_teardown):
    b = Calculation("b", 8)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b
    assert saved_items[0].result() == 8


def test_str_result_constant(common_setup_teardown):
    a = Calculation("a", 5.2)
    assert a.str_result() == " 5.2"


def test_str_result_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Calculation("c", a + b)
    assert c.str_result() == " 9"


def test_str_result_with_unit(common_setup_teardown):
    a = Calculation("a", 5.2, "in")
    assert a.str_result_with_unit() == " 5.2 \ \mathrm{in}"


def test_str_result_with_unit_without_unit(common_setup_teardown):
    a = Calculation("a", 5.2)
    assert a.str_result_with_unit() == " 5.2 \ \mathrm{}"


def test_str_sym_constant(common_setup_teardown):
    a = Calculation("a", -5, "mm^2")
    assert a.str_symbolic() == "{-5}"


def test_str_sym_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Calculation("c", a + b)
    assert c.str_symbolic() == "{a} + {b}"


def test_str_sym_expression_displays_a_single_level_deep(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    d = Calculation("d", a - c)
    assert d.str_symbolic() == "{a} - {c}"


def test_str_sub_constant(common_setup_teardown):
    a = Calculation("a", -5, "mm^2")
    assert a.str_substituted() == r"\left( -5 \right) \ \mathrm{}"


def test_str_sub_expression(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    c = Calculation("c", a + b)
    assert c.str_substituted() == r" 2 \ \mathrm{mm} +  7 \ \mathrm{mm}"


def test_str_sub_expression_displays_a_single_level_deep(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    d = Calculation("d", a - c)
    assert d.str_substituted() == " 2 \ \mathrm{} -  5 \ \mathrm{}"


# TODO: this could be improved
def test_to_str_constant(common_setup_teardown):
    a = Calculation("a", -5, "mm^2")
    assert (
        str(a)
        == r"a = {-5} = \left( -5 \right) \ \mathrm{} = \left(-5\right) \ \mathrm{mm^2}"
    )


def test_to_str_expression(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    c = Calculation("c", a + b)
    assert (
        str(c)
        == r"c = {a} + {b} =  2 \ \mathrm{mm} +  7 \ \mathrm{mm} =  9 \ \mathrm{}"
    )


def test_estimate_display_length_number(common_setup_teardown):
    a = Calculation("a", 5, "mm^2")
    assert a.estimate_display_length() == CalculationLength.NUMBER


def test_estimate_display_length_short(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    c = Calculation("c", a + b)
    assert c.estimate_display_length() == CalculationLength.SHORT


def test_estimate_display_length_long(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    d = Calculation("d", a - c + b * a * c + b - c - a - b)
    assert d.estimate_display_length() == CalculationLength.LONG
