import pytest

from efficalc import (
    Input,
    clear_all_input_default_overrides,
    get_all_calc_objects,
    reset_results,
    set_input_default_overrides,
)


@pytest.fixture
def common_setup_teardown():
    data = 5  # Set up a sample number
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    reset_results()


def test_default_value(common_setup_teardown):
    a = Input("a", 5)
    assert a.get_value() == 5


def test_save_calc_item(common_setup_teardown):
    b = Input("b", 8)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b


def test_str_result(common_setup_teardown):
    a = Input("a", 5.2)
    assert a.str_result() == " 5.2"


def test_str_result_with_unit(common_setup_teardown):
    a = Input("a", 5.2, "in")
    assert a.str_result_with_unit() == " 5.2 \ \mathrm{in}"


def test_str_result_with_unit_without_unit(common_setup_teardown):
    a = Input("a", 5.2)
    assert a.str_result_with_unit() == " 5.2 \ \mathrm{}"


def test_str_result_with_name(common_setup_teardown):
    a = Input("a_{chars}", 5.2, "in")
    assert a.str_result_with_name() == "a_{chars} = \  5.2 \ \mathrm{in}"


def test_str_sym(common_setup_teardown):
    a = Input("a", -5, "mm^2")
    assert a.str_symbolic() == "{a}"


def test_str_sub(common_setup_teardown):
    a = Input("a", -5, "mm^2")
    assert a.str_substituted() == r"\left( -5 \right) \ \mathrm{mm^2}"


# TODO: upgrade latexexpr_efficalc to allow string input vals
# def test_to_str_nan(common_setup_teardown):
#     a = Input("a", "test", "mm^2")
#     assert str(a) == "\mathrm{a} = \mathrm{test} \ \mathrm{mm^2}"


def test_to_str_number(common_setup_teardown):
    a = Input("a", -5, "mm^2")
    assert str(a) == r"a = \left( -5 \right) \ \mathrm{mm^2}"


def test_override_value(common_setup_teardown):
    set_input_default_overrides({"a": 123})
    a = Input("a", 5, "in")
    assert a.get_value() == 123
    assert a.str_result_with_name() == "a = \  123 \ \mathrm{in}"
    assert a.str_substituted() == r" 123 \ \mathrm{in}"
    assert str(a) == r"a =  123 \ \mathrm{in}"
