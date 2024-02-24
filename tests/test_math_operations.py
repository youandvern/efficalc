import math

import pytest
from latexexpr_efficalc import sum_elements

from efficalc import (
    Calculation,
    Input,
    a_brackets,
    brackets,
    c_brackets,
    cos,
    cosh,
    exp,
    ln,
    log,
    log10,
    maximum,
    minimum,
    r_brackets,
    reset_results,
    s_brackets,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
)


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    reset_results()


@pytest.fixture
def calculation_2():
    a = Input("a", 1)
    b = Input("b", 1)
    c = Calculation("c", a + b)
    yield c  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    reset_results()


@pytest.fixture
def calculation_3():
    a = Input("a", 1)
    b = Input("b", 2)
    c = Calculation("c", a + b)
    yield c  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    reset_results()


@pytest.fixture
def calculation_5():
    a = Input("a", 3)
    b = Input("b", 2)
    c = Calculation("c", a + b)
    yield c  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    reset_results()


#
# Input tests
#


def test_input_add(common_setup_teardown):
    a = Input("a", 5)
    c = a + a
    assert c.result() == 10


def test_input_add_right(common_setup_teardown):
    a = Input("a", 5)
    c = 2 + a
    assert c.result() == 7


def test_input_add_left(common_setup_teardown):
    a = Input("a", 5)
    c = a + 2
    assert c.result() == 7


def test_input_subtract(common_setup_teardown):
    a = Input("a", 5)
    c = a - a
    assert c.result() == 0


def test_input_subtract_right(common_setup_teardown):
    a = Input("a", 5)
    c = 7 - a
    assert c.result() == 2


def test_input_subtract_left(common_setup_teardown):
    a = Input("a", 5)
    c = a - 7
    assert c.result() == -2


def test_input_multiply(common_setup_teardown):
    a = Input("a", 5)
    c = a * a
    assert c.result() == 25


def test_input_multiply_right(common_setup_teardown):
    a = Input("a", 5)
    c = 2 * a
    assert c.result() == 10


def test_input_multiply_left(common_setup_teardown):
    a = Input("a", 5)
    c = a * 2
    assert c.result() == 10


def test_input_power(common_setup_teardown):
    a = Input("a", 5)
    b = Input("b", 3)
    c = a**b
    assert c.result() == 125


def test_input_power_right(common_setup_teardown):
    a = Input("a", 5)
    c = 2**a
    assert c.result() == 32


def test_input_power_left(common_setup_teardown):
    a = Input("a", 5)
    c = a**2
    assert c.result() == 25


def test_input_divide(common_setup_teardown):
    a = Input("a", 5)
    c = a / a
    assert c.result() == 1


def test_input_divide_right(common_setup_teardown):
    a = Input("a", 5)
    c = 10 / a
    assert c.result() == 2


def test_input_divide_left(common_setup_teardown):
    a = Input("a", 5)
    c = a / 2
    assert c.result() == 2.5


def test_input_floor_div(common_setup_teardown):
    a = Input("a", 5)
    b = Input("b", 2)
    c = a // b
    assert c.result() == 2


def test_input_neg(common_setup_teardown):
    a = Input("a", 5)
    assert (-a).result() == -5


def test_input_abs(common_setup_teardown):
    a = Input("a", -5)
    assert abs(a).result() == 5


def test_input_sum(common_setup_teardown):
    a = Input("a", 5)
    b = Input("b", 15)
    c = Input("c", 2)
    assert sum_elements(a, b, c).result() == 22


def test_input_max(common_setup_teardown):
    a = Input("a", 5)
    b = Input("b", 15)
    c = Input("c", 2)
    assert maximum(a, b, c).result() == 15


def test_input_min(common_setup_teardown):
    a = Input("a", 5)
    b = Input("b", 15)
    c = Input("c", 2)
    assert minimum(a, b, c).result() == 2


def test_input_sqrt(common_setup_teardown):
    a = Input("a", 25)
    assert sqrt(a).result() == 5


def test_input_sin(common_setup_teardown):
    a = Input("a", math.pi / 2)
    assert sin(a).result() == pytest.approx(1, abs=0.001)


def test_input_cos(common_setup_teardown):
    a = Input("a", math.pi / 2)
    assert cos(a).result() == pytest.approx(0, abs=0.001)


def test_input_tan(common_setup_teardown):
    a = Input("a", math.pi / 3)
    assert tan(a).result() == pytest.approx(1.732050, abs=0.001)


def test_input_sinh(common_setup_teardown):
    a = Input("a", -2)
    assert sinh(a).result() == pytest.approx(-3.62686, abs=0.001)


def test_input_cosh(common_setup_teardown):
    a = Input("a", -2)
    assert cosh(a).result() == pytest.approx(3.762196, abs=0.001)


def test_input_tanh(common_setup_teardown):
    a = Input("a", -2)
    assert tanh(a).result() == pytest.approx(-0.96403, abs=0.001)


def test_input_exp(common_setup_teardown):
    a = Input("a", 2)
    assert exp(a).result() == pytest.approx(math.e**2, abs=0.001)


def test_input_log(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 64)
    assert log(a, b).result() == 6


def test_input_ln(common_setup_teardown):
    a = Input("a", 2)
    assert ln(a).result() == pytest.approx(0.693147, abs=0.001)


def test_input_log10(common_setup_teardown):
    a = Input("a", 10000)
    assert log10(a).result() == 4


def test_input_r_brackets(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3, "in")
    c = b * r_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right)"
    )


def test_input_brackets(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3, "in")
    c = b * brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right)"
    )


def test_input_s_brackets(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3, "in")
    c = b * s_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left[  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right]"
    )


def test_input_c_brackets(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3, "in")
    c = b * c_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left\\{  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right\\}"
    )


def test_input_a_brackets(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3, "in")
    c = b * a_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left\\langle  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right\\rangle"
    )


#
# Calculation tests
#


def test_calculation_add(calculation_2, calculation_3):

    assert (calculation_2 + calculation_3).result() == 5


def test_calculation_add_right(calculation_3):
    c = 2 + calculation_3
    assert c.result() == 5


def test_calculation_add_left(calculation_5):
    c = calculation_5 + 2
    assert c.result() == 7


def test_calculation_subtract(calculation_2):
    c = calculation_2 - calculation_2
    assert c.result() == 0


def test_calculation_subtract_right(calculation_3):
    c = 7 - calculation_3
    assert c.result() == 4


def test_calculation_subtract_left(calculation_5):
    c = calculation_5 - 7
    assert c.result() == -2


def test_calculation_multiply(calculation_5):
    c = calculation_5 * calculation_5
    assert c.result() == 25


def test_calculation_multiply_right(calculation_5):
    c = 2 * calculation_5
    assert c.result() == 10


def test_calculation_multiply_left(calculation_5):
    c = calculation_5 * 2
    assert c.result() == 10


def test_calculation_power(calculation_2, calculation_3):
    c = calculation_2**calculation_3
    assert c.result() == 8


def test_calculation_power_right(calculation_3):
    c = 2**calculation_3
    assert c.result() == 8


def test_calculation_power_left(calculation_3):
    c = calculation_3**2
    assert c.result() == 9


def test_calculation_divide(calculation_2, calculation_3):
    c = calculation_3 / calculation_2
    assert c.result() == 1.5


def test_calculation_divide_right(calculation_5):
    c = 10 / calculation_5
    assert c.result() == 2


def test_calculation_divide_left(calculation_5):
    c = calculation_5 / 2
    assert c.result() == 2.5


def test_calculation_floor_div(calculation_2, calculation_5):
    c = calculation_5 // calculation_2
    assert c.result() == 2


def test_calculation_neg(calculation_5):
    assert (-calculation_5).result() == -5


def test_calculation_abs(calculation_5):
    negative_5 = Calculation("a", -1 * calculation_5)
    assert abs(negative_5).result() == 5


def test_calculation_sum(calculation_2, calculation_3, calculation_5):
    assert sum_elements(calculation_2, calculation_3, calculation_5).result() == 10


def test_calculation_max(calculation_2, calculation_3, calculation_5):
    assert maximum(calculation_2, calculation_5, calculation_3).result() == 5


def test_calculation_min(calculation_2, calculation_3, calculation_5):
    assert minimum(calculation_5, calculation_3, calculation_2).result() == 2


def test_calculation_sqrt(calculation_3):
    square_3 = Calculation("a", calculation_3 * calculation_3)
    assert sqrt(square_3).result() == 3


def test_calculation_sin(common_setup_teardown):
    a = Input("a", math.pi)
    calc = Calculation("c", a / 2)
    assert sin(calc).result() == pytest.approx(1, abs=0.001)


def test_calculation_cos(common_setup_teardown):
    a = Input("a", math.pi)
    calc = Calculation("c", a / 2)
    assert cos(calc).result() == pytest.approx(0, abs=0.001)


def test_calculation_tan(common_setup_teardown):
    a = Input("a", math.pi)
    calc = Calculation("c", a / 3)
    assert tan(calc).result() == pytest.approx(1.732050, abs=0.001)


def test_calculation_sinh(calculation_2):
    calc = Calculation("c", -1 * calculation_2)
    assert sinh(calc).result() == pytest.approx(-3.62686, abs=0.001)


def test_calculation_cosh(calculation_2):
    calc = Calculation("c", -1 * calculation_2)
    assert cosh(calc).result() == pytest.approx(3.762196, abs=0.001)


def test_calculation_tanh(calculation_2):
    calc = Calculation("c", -1 * calculation_2)
    assert tanh(calc).result() == pytest.approx(-0.96403, abs=0.001)


def test_calculation_exp(calculation_2):
    assert exp(calculation_2).result() == pytest.approx(math.e**2, abs=0.001)


def test_calculation_log(calculation_2):
    a = Input("a", 32)
    calc_64 = Calculation("c", a * 2)
    assert log(calculation_2, calc_64).result() == 6


def test_calculation_ln(calculation_2):
    assert ln(calculation_2).result() == pytest.approx(0.693147, abs=0.001)


def test_calculation_log10(common_setup_teardown):
    a = Input("a", 5000)
    calc = Calculation("c", a * 2)
    assert log10(calc).result() == 4


def test_calculation_r_brackets(calculation_2, calculation_3):
    c = calculation_3 * r_brackets(calculation_2 + calculation_3)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{} \\right)"
    )


def test_calculation_brackets(calculation_2, calculation_3):
    c = calculation_3 * brackets(calculation_2 + calculation_3)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{} \\right)"
    )


def test_calculation_s_brackets(calculation_2, calculation_3):
    c = calculation_3 * s_brackets(calculation_2 + calculation_3)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{} \\cdot \\left[  2 \\ \\mathrm{} +  3 \\ \\mathrm{} \\right]"
    )


def test_calculation_c_brackets(calculation_2, calculation_3):
    c = calculation_3 * c_brackets(calculation_2 + calculation_3)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{} \\cdot \\left\\{  2 \\ \\mathrm{} +  3 \\ \\mathrm{} \\right\\}"
    )


def test_calculation_a_brackets(calculation_2, calculation_3):
    c = calculation_3 * a_brackets(calculation_2 + calculation_3)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{} \\cdot \\left\\langle  2 \\ \\mathrm{} +  3 \\ \\mathrm{} \\right\\rangle"
    )
