from efficalc.canvas import Text


def test_text_defaults():
    t = Text("Hello, World!", 10, 20)
    svg = t.to_svg()
    assert "<text " in svg
    assert 'x="0"' in svg
    assert 'y="0"' in svg
    assert 'transform="translate(10, 20) rotate(0)"' in svg
    assert 'font-size="auto"' not in svg
    assert "text-anchor" not in svg
    assert "dominant-baseline" not in svg
    assert 'fill="black"' in svg
    assert 'stroke="none"' in svg
    assert 'stroke-width="0"' in svg
    assert ">Hello, World!</text>" in svg


def test_text_custom_style():
    t = Text(
        "Hello, World!",
        10,
        20,
        font_size="16px",
        rotate=45,
        horizontal_base="center",
        vertical_base="middle",
        fill="red",
        stroke="blue",
        stroke_width=2,
    )
    svg = t.to_svg()
    assert "<text " in svg
    assert 'x="0"' in svg
    assert 'y="0"' in svg
    assert 'transform="translate(10, 20) rotate(45)"' in svg
    assert 'font-size="16px"' in svg
    assert 'text-anchor="middle"' in svg
    assert 'dominant-baseline="middle"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="2"' in svg
    assert ">Hello, World!</text>" in svg


def test_text_horizontal_base():
    t = Text("Hello, World!", 10, 20, horizontal_base="end")
    svg = t.to_svg()
    assert "<text " in svg
    assert 'text-anchor="end"' in svg


def test_text_vertical_base():
    t = Text("Hello, World!", 10, 20, vertical_base="top")
    svg = t.to_svg()
    assert "<text " in svg
    assert 'dominant-baseline="hanging"' in svg
