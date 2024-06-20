from efficalc.canvas import Ellipse


def test_ellipse_defaults():
    e = Ellipse(1, 2, 3, 4)
    svg = e.to_svg()
    assert "<ellipse " in svg
    assert 'cx="1"' in svg
    assert 'cy="2"' in svg
    assert 'rx="3"' in svg
    assert 'ry="4"' in svg
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg
    assert " />" in svg


def test_ellipse_custom_style():
    e = Ellipse(1, 2, 3, 4, fill="red", stroke="blue", stroke_width=5)
    svg = e.to_svg()
    assert "<ellipse " in svg
    assert 'cx="1"' in svg
    assert 'cy="2"' in svg
    assert 'rx="3"' in svg
    assert 'ry="4"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert " />" in svg
