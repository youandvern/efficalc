import pytest
from latexexpr_efficalc import Variable

from efficalc import (
    Calculation,
    CalculationLength,
    Input,
    Symbolic,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
    sqrt,
)


@pytest.fixture
def common_setup_teardown():
    yield 5  # Provide some data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


def test_public_members(common_setup_teardown):
    a = Symbolic("a", 5, description="test desc", reference="a ref", result_check=True)
    assert a.name == "a"
    assert a.operation.result() == 5
    assert a.description == "test desc"
    assert a.reference == "a ref"
    assert a.result_check is True
    assert a.error is None


def test_value_constant(common_setup_teardown):
    a = Symbolic("a", 5)
    assert a.get_value() == 5
    assert a.result() == 5


def test_value_string(common_setup_teardown):
    a = Symbolic("a", "a str")
    assert a.get_value() == 0.0
    assert a.result() == 0.0


def test_value_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Symbolic("c", a + b)

    assert c.get_value() == 9
    assert c.result() == 9


def test_value_expression_with_calc(common_setup_teardown):
    a = Input("a", 2)
    b = Calculation("b", a * 7)
    c = Symbolic("c", a + b)

    assert c.get_value() == 16
    assert c.result() == 16


def test_result_value_error(common_setup_teardown):
    a = Input("a", -2)
    b = Symbolic("b", sqrt(a))
    assert b.str_symbolic() == "\\sqrt{ {a} }"
    assert b.error is None
    assert b.result() == 0.0
    assert "could not be calculated" in b.error


def test_save_calc_item(common_setup_teardown):
    b = Symbolic("b", 8)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b
    assert str(saved_items[0]) == "b = {8}"
    assert saved_items[0].result() == 8


def test_str_sym_constant(common_setup_teardown):
    a = Symbolic("a", 5)
    assert a.str_symbolic() == "{5}"
    assert a.str_substituted() == a.str_symbolic()


def test_str_sym_string(common_setup_teardown):
    a = Symbolic("a", "a str")
    assert a.str_symbolic() == "{a str}"
    assert a.str_substituted() == a.str_symbolic()


def test_str_sym_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Symbolic("c", a + b)

    assert c.str_symbolic() == "{a} + {b}"
    assert c.str_substituted() == c.str_symbolic()


def test_str_sym_expression_with_variables(common_setup_teardown):
    a = Variable("a")
    b = Variable("b")
    c = Symbolic("c", a + b)

    assert c.str_symbolic() == "{a} + {b}"
    assert c.str_substituted() == c.str_symbolic()


def test_str_sym_expression_with_calc(common_setup_teardown):
    a = Input("a", 2)
    b = Calculation("b", a * 7)
    c = Symbolic("c", a + b)

    assert c.str_symbolic() == "{a} + {b}"
    assert c.str_substituted() == c.str_symbolic()


def test_str_sym_expression_displays_only_one_level_deep(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    d = Symbolic("d", a - c)
    assert d.str_symbolic() == "{a} - {c}"
    assert d.str_substituted() == d.str_symbolic()


def test_str_result_with_description(common_setup_teardown):
    a = Symbolic("a", 5, description="test desc")
    assert a.str_result_with_description() == "test desc; a = {5}"


def test_to_str_constant(common_setup_teardown):
    a = Symbolic("a", 5)
    assert str(a) == "a = {5}"


def test_to_str_string(common_setup_teardown):
    a = Symbolic("a", "a str")
    assert str(a) == "a = {a str}"


def test_to_str_expression(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 7)
    c = Symbolic("c", a + b)

    assert str(c) == "c = {a} + {b}"


def test_to_str_expression_with_calc(common_setup_teardown):
    a = Input("a", 2)
    b = Calculation("b", a * 7)
    c = Symbolic("c", a + b)

    assert str(c) == "c = {a} + {b}"


def test_estimate_display_length_number(common_setup_teardown):
    a = Symbolic("a", 5, "mm^2")
    assert a.estimate_display_length() == CalculationLength.SHORT


def test_estimate_display_length_short(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    c = Symbolic("c", a + b)
    assert c.estimate_display_length() == CalculationLength.SHORT


def test_estimate_display_length_long(common_setup_teardown):
    a = Input("variable a", 2)
    b = Input("variable b", 3)
    c = Calculation("variable c", a + b)
    d = Symbolic("d", a - c + b * a * c + b - c - a - b)
    assert d.estimate_display_length() == CalculationLength.LONG
