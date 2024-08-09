import html

from efficalc import (
    Assumption,
    Calculation,
    CalculationLength,
    Comparison,
    ComparisonStatement,
    FigureBase,
    Heading,
    Input,
    Symbolic,
    Table,
    TextBlock,
    Title,
)
from efficalc.canvas import Canvas

CALC_MARGIN = "margin-left: 2rem;"
ALIGN = "&"
LINE_BREAK = r"\\[4pt]"
CALC_ITEM_WRAPPER_CLASS = "calc-item"


def generate_html_for_calc_items(calculation_items: list) -> str:
    """Generates a string containing HTML elements for displaying the provided calculation items. The calculations
    within the HTML elements will be written as plain LaTex to be reformatted via a polyfill or other formatter.

    :param calculation_items: A list of calculation items to generate the HTML for.
    :type calculation_items: list
    :return: HTML for the provided calculation items.
    :rtype: str
    """
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
            f'<span style="padding-right:0.5rem;">[ASSUME]</span> {_esc(calculation_item.text)}',
            CALC_MARGIN,
        )

    elif isinstance(calculation_item, Calculation):
        return _generate_calculation_html(calculation_item)

    elif isinstance(calculation_item, Canvas):
        return _generate_canvas_html(calculation_item)

    elif isinstance(calculation_item, Comparison):
        return _generate_comparison_html(calculation_item)

    elif isinstance(calculation_item, ComparisonStatement):
        return _generate_comparison_statement_html(calculation_item)

    elif isinstance(calculation_item, FigureBase):
        return _generate_figure_html(calculation_item)

    elif isinstance(calculation_item, Heading):
        heading_text = _esc(calculation_item.text)
        if calculation_item.numbered:
            number = ".".join(map(str, header_numbers)) + "."
            text = f"{number}\u00A0 {heading_text}"
        else:
            text = heading_text

        heading_size = min(4, max(1, calculation_item.head_level) + 1)

        return _wrap_h(text, heading_size)

    elif isinstance(calculation_item, Input):
        return _generate_input_html(calculation_item)

    elif isinstance(calculation_item, Symbolic):
        return _generate_symbolic_html(calculation_item)

    elif isinstance(calculation_item, Table):
        return _generate_result_table_html(calculation_item)

    elif isinstance(calculation_item, TextBlock):
        return _wrap_with_reference(
            _wrap_p(_esc(calculation_item.text)), _esc(calculation_item.reference)
        )

    elif isinstance(calculation_item, Title):
        return _wrap_h(_esc(calculation_item.text), 1)

    else:
        return _esc(str(calculation_item))


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

    description = _esc(item.description)
    if description is not None and description != "":
        calc_html += _wrap_p(description, CALC_MARGIN)

    item.result()
    if item.error is not None and item.error != "":
        calc_html += _wrap_p(
            f"<b>ERROR:</b>{_esc(item.error)}", f"color: red; {CALC_MARGIN}"
        )

    display_length = item.estimate_display_length()
    item_name = _esc(item.name)
    str_with_unit = _esc(item.str_result_with_unit())

    if display_length == CalculationLength.NUMBER:
        calc_tex = _wrap_math_inline(f"{item_name} = {str_with_unit}")

    elif display_length == CalculationLength.SHORT:
        str_symbolic = _esc(item.str_symbolic())
        str_substituted = _esc(item.str_substituted())

        calc_tex = _wrap_math(
            _wrap_alignment(
                f"{item_name} {ALIGN}= {str_symbolic} = {str_substituted} {LINE_BREAK} {ALIGN} \\therefore {item_name} = {str_with_unit}"
            )
        )

    else:
        str_symbolic = _esc(item.str_symbolic())
        str_substituted = _esc(item.str_substituted())

        calc_tex = _wrap_math(
            _wrap_alignment(
                f"{item_name} {ALIGN}= {str_symbolic} {LINE_BREAK} {ALIGN}= {str_substituted} {LINE_BREAK} {ALIGN}\\therefore {item_name} = {str_with_unit}"
            )
        )

    calc_html += _wrap_with_reference(_wrap_p(calc_tex), _esc(item.reference))

    return _wrap_div(calc_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_symbolic_html(item: Symbolic) -> str:
    calc_html = ""

    description = _esc(item.description)
    if description is not None and description != "":
        calc_html += _wrap_p(description, CALC_MARGIN)

    if item.error is not None and item.error != "":
        calc_html += _wrap_p(
            f"<b>ERROR:</b>{_esc(item.error)}", f"color: red; {CALC_MARGIN}"
        )

    item_name = _esc(item.name)
    str_symbolic = _esc(item.str_symbolic())

    calc_tex = _wrap_math(f"{item_name} = {str_symbolic}")
    calc_html += _wrap_with_reference(_wrap_p(calc_tex), _esc(item.reference))

    return _wrap_div(calc_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_comparison_html(item: Comparison) -> str:
    comp_html = ""
    description = _esc(item.description)

    if description is not None and description != "":
        comp_html += _wrap_p(description, CALC_MARGIN)

    symbolic = _esc(item.str_symbolic())
    substituted = _esc(item.str_substituted())
    sym_and_sub = (
        f"{symbolic} {LINE_BREAK} {substituted}"
        if symbolic != substituted
        else substituted
    )
    comp_html += _wrap_with_reference(
        _wrap_p(
            _wrap_math(
                _wrap_alignment(
                    f"Check {sym_and_sub} {LINE_BREAK} {ALIGN}\\therefore {_esc(item.get_message())}"
                )
            )
        ),
        _esc(item.reference),
    )

    return _wrap_div(comp_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_result_table_html(item: Table) -> str:
    full_width = " width:100%;" if item.full_width else ""
    striped_class = ' class="striped"' if item.striped else ""
    style = f' style="margin:auto;{full_width}"'
    table_html = f"<table{striped_class}{style}>"
    if item.title:
        table_html += f"<caption><b>{item.title}</b></caption>"
    if item.headers:
        table_html += "<thead><tr>"
        for header in item.headers:
            table_html += f"<th>{header}</th>"
        table_html += "</tr></thead>"
    table_html += "<tbody>"
    for row in item.data:
        table_html += "<tr>"
        for cell in row:
            table_html += f"<td>{cell}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return _wrap_div(table_html, CALC_MARGIN, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_comparison_statement_html(item: ComparisonStatement) -> str:
    comp_html = ""
    description = _esc(item.description)

    if description is not None and description != "":
        comp_html += _wrap_p(description, CALC_MARGIN)

    comp_html += _wrap_with_reference(
        _wrap_p(_wrap_math(f"\\rightarrow {_esc(item.str_symbolic())}")),
        _esc(item.reference),
    )

    return _wrap_div(comp_html, class_name=CALC_ITEM_WRAPPER_CLASS)


def _generate_figure_html(item: FigureBase) -> str:
    try:
        base64_figure = item.get_base64_str()
    except Exception as e:
        return _wrap_p(
            f"<b>There was an error loading this image:</b>{e}",
            f"color: red; {CALC_MARGIN}",
        )

    caption = _esc(item.caption)
    base64_figure = _esc(base64_figure)
    return _wrap_fig(
        _wrap_img_base64(base64_figure, caption, item.full_width)
        + _wrap_caption(caption)
    )


def _generate_input_html(item: Input) -> str:

    description = (
        _wrap_p(f" ", "width:40px;")
        if not item.description
        else _wrap_p(f"{_esc(item.description)};", "width:350px;")
    )

    tex = _wrap_p(
        _wrap_math_inline(_esc(str(item))),
        "display:inline-block; margin-bottom:1rem; margin-left: 3rem",
    )

    return _wrap_with_reference(
        _wrap_div(
            f"{description} {tex}",
            "display:flex; flex-direction:row; justify-content:flex-start",
        ),
        _esc(item.reference),
    )


def _generate_canvas_html(item: Canvas) -> str:
    text_align = " text-align:center;" if item.centered else ""
    caption = (
        f'<p style="color:#6f6f6f;{text_align} font-size:0.9em;">{item.caption}</p>'
        if item.caption
        else ""
    )
    return _wrap_div(item.to_svg() + caption, f"margin-bottom:2rem; {CALC_MARGIN}")


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


def _wrap_fig(html_content: str) -> str:
    return f"<figure>{html_content}</figure>"


def _wrap_img_base64(
    img_base64: str, description: str = None, full_width: bool = False
) -> str:
    alt_text = "Calculation figure" if description is None else description
    full_width_style = "width:100%;" if full_width else ""
    return f'<img src="data:image/png;base64,{img_base64}" alt="{alt_text}" style="max-width:100%; {full_width_style}"/>'


def _wrap_caption(caption: str) -> str:
    if caption is None:
        return ""
    return f'<figcaption style="color:#6f6f6f; font-size:0.9em;">{caption}</figcaption>'


def _esc(user_text: str | None) -> str | None:
    if user_text is None:
        return None
    """Escape HTML special characters."""
    return html.escape(user_text)
