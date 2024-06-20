from efficalc.canvas import Rectangle


def test_rectangle_defaults():
    r = Rectangle(1, 2, 3, 4)
    svg = r.to_svg()
    assert "<rect " in svg
    assert 'x="1"' in svg
    assert 'y="2"' in svg
    assert 'width="3"' in svg
    assert 'height="4"' in svg
    assert 'rx="0"' in svg
    assert 'ry="0"' in svg
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg
    assert " />" in svg


def test_rectangle_rounded_corners():
    r = Rectangle(1, 2, 3, 4, rx=5, ry=6)
    svg = r.to_svg()
    assert "<rect " in svg
    assert 'x="1"' in svg
    assert 'y="2"' in svg
    assert 'width="3"' in svg
    assert 'height="4"' in svg
    assert 'rx="5"' in svg
    assert 'ry="6"' in svg
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg
    assert " />" in svg


def test_rectangle_custom_style():
    r = Rectangle(1, 2, 3, 4, fill="red", stroke="blue", stroke_width=5)
    svg = r.to_svg()
    assert "<rect " in svg
    assert 'x="1"' in svg
    assert 'y="2"' in svg
    assert 'width="3"' in svg
    assert 'height="4"' in svg
    assert 'rx="0"' in svg
    assert 'ry="0"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert " />" in svg
