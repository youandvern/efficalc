import pytest
from latexexpr_efficalc import brackets

from efficalc import (
    Assumption,
    Calculation,
    CalculationLength,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    TextBlock,
    Title,
    clear_saved_objects,
)
from efficalc.generate_html import generate_html_for_calc_items


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


def test_assumption(common_setup_teardown):
    a = Assumption("the text")
    result = generate_html_for_calc_items([a])
    assert "[ASSUME]" in result
    assert a.text in result


def test_calculation_number(common_setup_teardown):
    a = Calculation("calc", 5, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([a])
    assert a.estimate_display_length() == CalculationLength.NUMBER
    assert a.description in result
    assert a.reference in result
    assert a.name in result
    assert a.str_result_with_unit() in result
    assert r"\therefore" not in result


def test_calculation_short(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    calc = Calculation("calc_1", a + b, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result


def test_calculation_long(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Calculation(
        "calc_1",
        a - c + brackets(b * a * c) + b - c - a - b,
        "in",
        "describing text",
        "refer to code",
    )
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.LONG
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result


def test_calculation_without_ref(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    calc = Calculation("calc_1", a + b, "in", "describing text")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result
    assert "[]" not in result  # empty reference tag


def test_calculation_error(common_setup_teardown):
    a = Input("a", 2, "mm")
    calc = Calculation("calc_1", a / 0, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result
    assert "ERROR:" in result
    assert "could not be calculated because zero was in the denominator." in result


def test_comparison_number(common_setup_teardown):

    calc = Comparison(5, ">", 2, "good", "nah", "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert calc.result() in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert r"\therefore" in result


def test_comparison_variable(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Comparison(a, ">", c, "good", "nah", "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert calc.result() in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert r"\therefore" in result


def test_comparison_without_ref(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Comparison(a, ">", c, "good", "nah", "a describer", "")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert ">" in result
    assert calc.result() in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert r"\therefore" in result
    assert "[]" not in result  # empty reference tag


def test_comparison_statement(common_setup_teardown):
    calc = ComparisonStatement(5, ">", 2, ">=", 1.5, "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert calc.str_symbolic() in result


def test_comparison_statement_without_ref(common_setup_teardown):
    calc = ComparisonStatement(5, ">", 2, ">=", 1.5, "a describer")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert ">" in result
    assert calc.str_symbolic() in result
    assert "[]" not in result  # empty reference tag


def test_heading_max_size(common_setup_teardown):
    h = Heading("the text", 0, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h2>" in result


def test_heading_mid_size(common_setup_teardown):
    h = Heading("the text", 2, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h3>" in result


def test_heading_min_size(common_setup_teardown):
    h = Heading("the text", 6, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h4>" in result


def test_heading_numbering(common_setup_teardown):
    h0 = Heading("Test 1.")
    h1 = Heading("Test 2.")
    h2 = Heading("Test 2.1.", 2)
    h3 = Heading("Test 2.2.", 2)
    h4 = Heading("Test 2.2.1.", 3)
    h5 = Heading("Test 2.2.1.1.", 4)
    h6 = Heading("Test 2.3.", 2)
    h7 = Heading("Test 2.3.1.", 3)
    h8 = Heading("Test 3.", 1)
    h9 = Heading("Test 4.", 1)
    h10 = Heading("Test 5.", 1)
    h11 = Heading("Test 5.1.1.1.", 4)
    result = generate_html_for_calc_items(
        [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11]
    )
    assert "1.\u00A0 Test 1." in result
    assert "2.\u00A0 Test 2." in result
    assert "2.1.\u00A0 Test 2.1." in result
    assert "2.2.\u00A0 Test 2.2." in result
    assert "2.2.1.\u00A0 Test 2.2.1." in result
    assert "2.2.1.1.\u00A0 Test 2.2.1.1." in result
    assert "2.3.\u00A0 Test 2.3." in result
    assert "2.3.1.\u00A0 Test 2.3.1." in result
    assert "3.\u00A0 Test 3." in result
    assert "4.\u00A0 Test 4." in result
    assert "5.\u00A0 Test 5." in result
    assert "5.1.1.1.\u00A0 Test 5.1.1.1." in result


def test_heading_no_numbering(common_setup_teardown):
    h0 = Heading("Test 1.", numbered=False)
    h1 = Heading("Test 2.", numbered=False)
    h2 = Heading("Test 2.1.", 2, numbered=False)
    h3 = Heading("Test 2.2.", 2, numbered=False)
    h4 = Heading("Test 2.2.1.", 3, numbered=False)
    h5 = Heading("Test 2.2.1.1.", 4, numbered=False)
    result = generate_html_for_calc_items([h0, h1, h2, h3, h4, h5])

    assert "1.\u00A0 Test 1." not in result
    assert "Test 1." in result

    assert "2.\u00A0 Test 2." not in result
    assert "Test 2." in result

    assert "2.1.\u00A0 Test 2.1." not in result
    assert "Test 2.1." in result

    assert "2.2.\u00A0 Test 2.2." not in result
    assert "Test 2.2." in result

    assert "2.2.1.\u00A0 Test 2.2.1." not in result
    assert "Test 2.2.1." in result

    assert "2.2.1.1.\u00A0 Test 2.2.1.1." not in result
    assert "Test 2.2.1.1." in result


def test_input(common_setup_teardown):
    a = Input("calc", 5, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([a])
    assert a.description in result
    assert "[" + a.reference + "]" in result
    assert a.name in result
    assert str(a) in result


def test_input_without_desc(common_setup_teardown):
    a = Input("calc", 5, "in", "", "refer to code")
    result = generate_html_for_calc_items([a])
    assert "[" + a.reference + "]" in result
    assert a.name in result
    assert str(a) in result


def test_input_without_ref(common_setup_teardown):
    a = Input("calc", 5, "in", "A variable")
    result = generate_html_for_calc_items([a])
    assert "]" not in result
    assert "[" not in result
    assert a.description in result
    assert a.name in result
    assert str(a) in result


def test_text_block(common_setup_teardown):
    a = TextBlock("the text", reference="any ref")
    result = generate_html_for_calc_items([a])
    assert a.text in result
    assert a.reference in result


def test_text_block_without_ref(common_setup_teardown):
    a = TextBlock("the text", reference="")
    b = TextBlock("the other text", reference=None)
    result = generate_html_for_calc_items([a, b])
    assert a.text in result
    assert b.text in result
    assert "[" not in result  # empty reference tag
    assert "]" not in result  # empty reference tag


def test_title(common_setup_teardown):
    a = Title("the text")
    result = generate_html_for_calc_items([a])
    assert a.text in result
    assert "<h1>" in result
