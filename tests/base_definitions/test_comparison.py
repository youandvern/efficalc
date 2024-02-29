import pytest

from efficalc import (
    Calculation,
    Comparison,
    Input,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
)


@pytest.fixture
def common_setup_teardown():
    data = 5  # Set up a sample number
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


def test_public_members(common_setup_teardown):
    a = Comparison(
        2,
        ">",
        4,
        true_message="yes",
        false_message="no",
        description="test desc",
        reference="a ref",
        result_check=False,
    )

    assert a.a == 2
    assert a.comparator == ">"
    assert a.b == 4
    assert a.true_message == "yes"
    assert a.false_message == "no"
    assert a.description == "test desc"
    assert a.reference == "a ref"
    assert a.result_check is False


def test_save_calc_item(common_setup_teardown):
    comp = Comparison(5, ">", 2.2)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == comp
    assert saved_items[0].is_passing() is True


def test_result_lt(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, "<", small)
    assert comp1.is_passing() is False
    assert comp1.result() == comp1.false_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, "<", large)
    assert comp2.is_passing() is True
    assert comp2.result() == comp2.true_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, "<", large_too)
    assert comp3.is_passing() is False
    assert comp3.result() == comp3.false_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_le(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, "<=", small)
    assert comp1.is_passing() is False
    assert comp1.result() == comp1.false_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, "<=", large)
    assert comp2.is_passing() is True
    assert comp2.result() == comp2.true_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, "<=", large_too)
    assert comp3.is_passing() is True
    assert comp3.result() == comp3.true_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_eq(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, "=", small)
    assert comp1.is_passing() is False
    assert comp1.result() == comp1.false_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, "=", large)
    assert comp2.is_passing() is False
    assert comp2.result() == comp2.false_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, "=", large_too)
    assert comp3.is_passing() is True
    assert comp3.result() == comp3.true_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_ne(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, "!=", small)
    assert comp1.is_passing() is True
    assert comp1.result() == comp1.true_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, "!=", large)
    assert comp2.is_passing() is True
    assert comp2.result() == comp2.true_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, "!=", large_too)
    assert comp3.is_passing() is False
    assert comp3.result() == comp3.false_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_gt(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, ">", small)
    assert comp1.is_passing() is True
    assert comp1.result() == comp1.true_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, ">", large)
    assert comp2.is_passing() is False
    assert comp2.result() == comp2.false_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, ">", large_too)
    assert comp3.is_passing() is False
    assert comp3.result() == comp3.false_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_ge(common_setup_teardown):
    small = Input("b", 2)
    large = Calculation("a", 5)
    large_too = Input("e", 5)

    comp1 = Comparison(large, ">=", small)
    assert comp1.is_passing() is True
    assert comp1.result() == comp1.true_message
    assert comp1.get_value() is comp1.is_passing()

    comp2 = Comparison(small, ">=", large)
    assert comp2.is_passing() is False
    assert comp2.result() == comp2.false_message
    assert comp2.get_value() is comp2.is_passing()

    comp3 = Comparison(large, ">=", large_too)
    assert comp3.is_passing() is True
    assert comp3.result() == comp3.true_message
    assert comp3.get_value() is comp3.is_passing()


def test_result_value_error(common_setup_teardown):
    comp = Comparison("text", ">=", 5)
    assert comp.is_passing() is False
    assert comp.result() == "Unable to compare text and 5 with operator >="


def test_str_sym_both_constant(common_setup_teardown):
    comp = Comparison(5, ">", 2.2)
    assert comp.str_symbolic() == comp.str_substituted()


def test_str_sym_left_constant(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    comp = Comparison(5, ">", a)
    assert comp.str_symbolic() == "\ 5 & > \ a"


def test_str_sym_right_constant(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    comp = Comparison(a, ">", 5)
    assert comp.str_symbolic() == "\ a & > \ 5"


def test_str_sym_all_vars(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    b = Calculation("b", 7, "in")
    comp = Comparison(a, ">", b)
    assert comp.str_symbolic() == "\ a & > \ b"


def test_str_sym_does_not_display_calculation(common_setup_teardown):
    a = Input("a", 3)
    b = Input("b", 12)
    calc = Calculation("calc", a + b, "in")
    comp = Comparison(a, ">", calc)
    assert comp.str_symbolic() == "\ a & > \ calc"


def test_str_sym_displays_valid_latex_operators(common_setup_teardown):

    assert Comparison(2, "<", 1).str_symbolic() == "\ 2 & < \ 1"
    assert Comparison(2, "<=", 1).str_symbolic() == "\ 2 & \leq \ 1"
    assert Comparison(2, "=", 1).str_symbolic() == "\ 2 & = \ 1"
    assert Comparison(2, "!=", 1).str_symbolic() == r"\ 2 & \neq \ 1"
    assert Comparison(2, "==", 1).str_symbolic() == "\ 2 & = \ 1"
    assert Comparison(2, ">", 1).str_symbolic() == "\ 2 & > \ 1"
    assert Comparison(2, ">=", 1).str_symbolic() == "\ 2 & \geq \ 1"


def test_str_sub_both_constant(common_setup_teardown):
    comp = Comparison(5, ">", 2.2)
    assert comp.str_substituted() == "\ 5 & > \ 2.2"


def test_str_sub_left_constant(common_setup_teardown):
    a = Calculation("a", 1.4)
    comp = Comparison(5, ">", a)
    assert comp.str_substituted() == "\ 5 & > \  1.4 \ \mathrm{}"


def test_str_sub_right_constant(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    comp = Comparison(a, ">", 5)
    assert comp.str_substituted() == "\  1.4 \ \mathrm{in} & > \ 5"


def test_str_sub_all_vars(common_setup_teardown):
    a = Calculation("a", 1.4, "in")
    b = Calculation("b", 7, "in")
    comp = Comparison(a, ">", b)
    assert comp.str_substituted() == "\  1.4 \ \mathrm{in} & > \  7 \ \mathrm{in}"


def test_str_sub_does_not_display_calculation(common_setup_teardown):
    a = Input("a", 3, "in")
    b = Input("b", 12)
    calc = Calculation("calc", a + b, "in")
    comp = Comparison(a, ">", calc)
    assert comp.str_substituted() == "\  3 \ \mathrm{in} & > \  15 \ \mathrm{in}"


def test_str_sub_displays_valid_latex_operators(common_setup_teardown):

    assert Comparison(2, "<", 1).str_substituted() == "\ 2 & < \ 1"
    assert Comparison(2, "<=", 1).str_substituted() == "\ 2 & \leq \ 1"
    assert Comparison(2, "=", 1).str_substituted() == "\ 2 & = \ 1"
    assert Comparison(2, "!=", 1).str_substituted() == r"\ 2 & \neq \ 1"
    assert Comparison(2, "==", 1).str_substituted() == "\ 2 & = \ 1"
    assert Comparison(2, ">", 1).str_substituted() == "\ 2 & > \ 1"
    assert Comparison(2, ">=", 1).str_substituted() == "\ 2 & \geq \ 1"


def test_to_str(common_setup_teardown):
    a = Input("a", 3, "in")
    comp = Comparison(a, ">", 2)
    assert (
        str(comp)
        == f"Check {comp.str_symbolic()} \\rightarrow {comp.str_substituted()} \\therefore {comp.result()}"
    )
