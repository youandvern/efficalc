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
)

CALC_MARGIN = "margin-left: 2rem;"
ALIGN = "&"
LINE_BREAK = r"\\[4pt]"
CALC_ITEM_WRAPPER_CLASS = "calc-item"


def generate_html_for_calc_items(calculation_items: list) -> str:
    header_numbers = [0]
    report_items_html = ""

    for item in calculation_items:
        if isinstance(item, Heading) and item.numbered:
            header_numbers = _increment_headers_and_get_next(
                header_numbers, item.head_level
            )

        report_items_html += _generate_html_for_calc_item(item, header_numbers)

    return report_items_html


def _generate_html_for_calc_item(calculation_item, header_numbers: list[int]) -> str:
    if isinstance(calculation_item, Assumption):
        return _wrap_p(
            f'<span style="padding-right:0.5rem;">[ASSUME]</span> {calculation_item.text}',
            CALC_MARGIN,
        )

    elif isinstance(calculation_item, Calculation):
        return _generate_calculation_html(calculation_item)

    elif isinstance(calculation_item, Comparison):
        return _generate_comparison_html(calculation_item)

    elif isinstance(calculation_item, ComparisonStatement):
        return _generate_comparison_statement_html(calculation_item)

    elif isinstance(calculation_item, Heading):
        if calculation_item.numbered:
            number = ".".join(map(str, header_numbers)) + "."
            text = f"{number}\u00A0 {calculation_item.text}"
        else:
            text = calculation_item.text

        heading_size = min(4, max(1, calculation_item.head_level) + 1)

        return _wrap_h(text, heading_size)

    elif isinstance(calculation_item, Input):
        return _generate_input_html(calculation_item)

    elif isinstance(calculation_item, TextBlock):
        return _wrap_with_reference(
            _wrap_p(calculation_item.text), calculation_item.reference
        )

    elif isinstance(calculation_item, Title):
        return _wrap_h(calculation_item.text, 1)


def _increment_headers_and_get_next(
    current_headers: list[int], next_level: int
) -> list[int]:

    if next_level < 1:
        next_level = 1

    current_size = len(current_headers)

    if next_level > current_size:
        new_headers = current_headers.copy()
        for i in range(current_size, next_level):
            new_headers.append(1)
        return new_headers
    else:
        new_headers = current_headers[:next_level]
        new_headers[next_level - 1] += 1
        return new_headers


def _generate_calculation_html(item: Calculation) -> str:
    calc_html = ""

    if item.description is not None and item.description != "":
        calc_html += _wrap_p(item.description, CALC_MARGIN)

    item.result()
    if item.error is not None and item.error != "":
        calc_html += _wrap_p(f"<b>ERROR:</b>{item.error}", f"color: red; {CALC_MARGIN}")

    display_length = item.estimate_display_length()
    if display_length == CalculationLength.NUMBER:
        calc_tex = _wrap_math_inline(f"{item.name} = {item.str_result_with_unit()}")
    elif display_length == CalculationLength.SHORT:
        calc_tex = _wrap_math(
            _wrap_alignment(
                f"{item.name} {ALIGN}= {item.str_symbolic()} = {item.str_substituted()} {LINE_BREAK} {ALIGN} \\therefore {item.name} = {item.str_result_with_unit()}"
            )
        )
    else:
        calc_tex = _wrap_math(
            _wrap_alignment(
                f"{item.name} {ALIGN}= {item.str_symbolic()} {LINE_BREAK} {ALIGN}= {item.str_substituted()} {LINE_BREAK} {ALIGN}\\therefore {item.name} = {item.str_result_with_unit()}"
            )
        )

    calc_html += _wrap_with_reference(_wrap_p(calc_tex), item.reference)

    return _wrap_div(calc_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_comparison_html(item: Comparison) -> str:
    comp_html = ""
    if item.description is not None and item.description != "":
        comp_html += _wrap_p(item.description, CALC_MARGIN)

    symbolic = item.str_symbolic()
    substituted = item.str_substituted()
    sym_and_sub = (
        f"{symbolic} {LINE_BREAK} {substituted}"
        if symbolic != substituted
        else substituted
    )
    comp_html += _wrap_with_reference(
        _wrap_p(
            _wrap_math(
                _wrap_alignment(
                    f"Check {sym_and_sub} {LINE_BREAK} {ALIGN}\\therefore {item.result()}"
                )
            )
        ),
        item.reference,
    )

    return _wrap_div(comp_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_comparison_statement_html(item: ComparisonStatement) -> str:
    comp_html = ""
    if item.description is not None and item.description != "":
        comp_html += _wrap_p(item.description, CALC_MARGIN)

    comp_html += _wrap_with_reference(
        _wrap_p(_wrap_math(f"\\rightarrow {item.str_symbolic()}")),
        item.reference,
    )

    return _wrap_div(comp_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_input_html(item: Input) -> str:

    description = (
        _wrap_p(f" ", "width:40px;")
        if not item.description
        else _wrap_p(f"{item.description};", "width:350px;")
    )

    tex = _wrap_p(
        _wrap_math_inline(str(item)),
        "display:inline-block; margin-bottom:1rem; margin-left: 3rem",
    )

    return _wrap_with_reference(
        _wrap_div(
            f"{description} {tex}",
            "display:flex; flex-direction:row; justify-content:flex-start",
        ),
        item.reference,
    )


def _wrap_math(content: str) -> str:
    return rf"\[ {content} \]"


def _wrap_math_inline(content: str) -> str:
    return rf"\( {content} \)"


def _wrap_with_reference(primary_content: str, reference: str | None) -> str:
    ref = _wrap_span(f"[{reference}]") if reference else ""
    vertical_justified = (
        "display: flex; flex-direction: column; justify-content: center;"
    )

    return _wrap_div(
        f"{_wrap_div(primary_content, vertical_justified)} {_wrap_div(ref, vertical_justified)}",
        f"display:flex; flex-direction:row; justify-content:space-between; {CALC_MARGIN}",
    )


def _wrap_alignment(content: str) -> str:
    begin = r"\begin{align}"
    end = r"\end{align}"
    return rf"{begin} {content} {end}"


def _wrap_p(content: str, style: str = None) -> str:
    if style is not None:
        return f'<p style="{style}">{content}</p>'
    return f"<p>{content}</p>"


def _wrap_span(content: str, style: str = None) -> str:
    if style is not None:
        return f'<span style="{style}">{content}</span>'
    return f"<span>{content}</span>"


def _wrap_div(content: str, style: str = None, class_name: str = None) -> str:
    class_tag = "" if class_name is None else f' class="{class_name}"'
    style_tag = "" if style is None else f' style="{style}"'
    return f"<div{class_tag}{style_tag}>{content}</div>"


def _wrap_h(content: str, level: int) -> str:
    return f"<h{level}>{content}</h{level}>"
