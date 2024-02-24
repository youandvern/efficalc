import pytest
from latexexpr_efficalc import Operation, Variable

from efficalc import (
    Calculation,
    ComparisonStatement,
    Input,
    clear_all_input_default_overrides,
    get_all_calc_objects,
    reset_results,
)


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    reset_results()


def test_save_calc_item(common_setup_teardown):
    comp = ComparisonStatement(5, ">", 2.2)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == comp
    assert saved_items[0].a == 5


def test_str_sym_2_constants(common_setup_teardown):
    comp = ComparisonStatement(5, ">", 2.2)
    assert comp.str_symbolic() == "5 \ > \ 2.2"


def test_str_sym_3_constants(common_setup_teardown):
    comp = ComparisonStatement(5, ">", 2.2, "<", 1)
    assert comp.str_symbolic() == "5 \ > \ 2.2 \ <  \ 1"


def test_str_sym_operation(common_setup_teardown):
    a = Variable("a", 5)
    b = Operation("", a**2)
    comp = ComparisonStatement(5, ">", b)
    assert comp.str_symbolic() == r"5 \ > \ {\left( {a} \right)}^{ {2} }"


def test_str_sym_constant_and_calc(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    comp = ComparisonStatement(5, ">", a)
    assert comp.str_symbolic() == "5 \ > \ a"


def test_str_sym_input_calc_constant(common_setup_teardown):
    a = Input("a", 2, "in")
    b = Calculation("b", 5 * a)
    comp = ComparisonStatement(a, ">", b, "<", 1)
    assert comp.str_symbolic() == "a \ > \ b \ <  \ 1"


def test_str_sym_does_not_display_calculation_when_name_exists(common_setup_teardown):
    a = Input("a", 3)
    b = Input("b", 12)
    calc = Calculation("calc", a + b, "in")
    comp = ComparisonStatement(a, ">", calc)
    assert comp.str_symbolic() == "a \ > \ calc"


def test_str_sym_displays_valid_latex_operators(common_setup_teardown):

    assert ComparisonStatement(2, "<", 1).str_symbolic() == "2 \ < \ 1"
    assert ComparisonStatement(2, "<=", 1).str_symbolic() == "2 \ \leq \ 1"
    assert ComparisonStatement(2, "=", 1).str_symbolic() == "2 \ = \ 1"
    assert ComparisonStatement(2, "!=", 1).str_symbolic() == r"2 \ \neq \ 1"
    assert ComparisonStatement(2, "==", 1).str_symbolic() == "2 \ = \ 1"
    assert ComparisonStatement(2, ">", 1).str_symbolic() == "2 \ > \ 1"
    assert ComparisonStatement(2, ">=", 1).str_symbolic() == "2 \ \geq \ 1"


def test_to_str(common_setup_teardown):
    a = Input("a", 3, "in")
    b = Calculation("b", a + 2)
    comp = ComparisonStatement(a, ">", 2, "<", b)
    assert str(comp) == comp.str_symbolic()
