from efficalc.canvas import Circle


def test_circle_defaults():
    r = Circle(1, 2, 3)
    svg = r.to_svg()
    assert "<circle " in svg
    assert 'cx="1"' in svg
    assert 'cy="2"' in svg
    assert 'r="3"' in svg
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg
    assert " />" in svg


def test_circle_custom_style():
    r = Circle(1, 2, 3, fill="red", stroke="blue", stroke_width=5)
    svg = r.to_svg()
    assert "<circle " in svg
    assert 'cx="1"' in svg
    assert 'cy="2"' in svg
    assert 'r="3"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert " />" in svg
