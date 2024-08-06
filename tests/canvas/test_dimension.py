from efficalc.canvas import Dimension, Line, Text


def test_dimension_defaults():
    d = Dimension(0, 0, 100, 0)
    svg = d.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert (
        '<line x1="0.0" y1="-10.0" x2="100.0" y2="-10.0" '
        'marker-start="url(#ArrowMarker-context-stroke-none-None-1-False-auto-start-reverse-point)" '
        'marker-end="url(#ArrowMarker-context-stroke-none-None-1-False-auto-point)" '
        'stroke-width="1" />'
    ) in svg
    assert (
        '<text x="0" y="0" transform="translate(50.0, -12.0) rotate(0.0)" font-size="7.0" '
        in svg
    )
    assert 'text-anchor="middle"' in svg
    assert 'dominant-baseline="text-top"' in svg
    assert "marker-start" in svg
    assert "marker-end" in svg
    assert ">100.00</text>" in svg


def test_dimension_with_text_override():
    d = Dimension(0, 0, 100, 0, text="Custom Text")
    svg = d.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert "<line" in svg
    assert '<text x="0" y="0"' in svg
    assert "Custom Text" in svg


def test_dimension_with_units():
    d = Dimension(0, 0, 100, 0, unit="cm")
    svg = d.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert "<line" in svg
    assert '<text x="0" y="0"' in svg
    assert "100.00cm" in svg


def test_dimension_with_offset():
    d = Dimension(0, 0, 100, 0, offset=20)
    svg = d.to_svg()
    assert "<g>" in svg
    assert '<line x1="0.0" y1="-20.0" x2="100.0" y2="-20.0" ' in svg
    assert '<line x1="0.0" y1="0.0" x2="0.0" y2="-24.0"' in svg
    assert '<text x="0" y="0"' in svg
    assert "translate(50.0, -22.0)" in svg


def test_dimension_with_gap():
    d = Dimension(0, 0, 100, 0, gap=3.25)
    svg = d.to_svg()
    assert "<g>" in svg
    assert '<line x1="0.0" y1="-10.0" x2="100.0" y2="-10.0" ' in svg
    assert '<line x1="0.0" y1="-3.25" x2="0.0" y2="-14.0"' in svg


def test_dimension_text_position_bottom():
    d = Dimension(0, 0, 100, 0, text_position="bottom")
    svg = d.to_svg()
    assert "<g>" in svg
    assert '<line x1="0.0" y1="-10.0" x2="100.0" y2="-10.0" ' in svg
    assert '<text x="0" y="0" transform="translate(50.0, -8.0) rotate(0.0)" ' in svg
    assert 'dominant-baseline="hanging"' in svg
    assert "100.00" in svg


def test_dimension_text_size():
    d = Dimension(0, 0, 100, 0, text_size=2)
    svg = d.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert '<line x1="0.0" y1="-10.0" x2="100.0" y2="-10.0" ' in svg
    assert '<text x="0" y="0"' in svg
    assert 'font-size="14"' in svg
    assert "100.00" in svg


def test_dimension_custom_style():
    d = Dimension(0, 0, 100, 0, stroke="blue", stroke_width=2)
    svg = d.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="2"' in svg
    assert '<line x1="0.0" y1="-10.0" x2="100.0" y2="-10.0" ' in svg
    assert '<text x="0" y="0"' in svg
    assert "100.00" in svg
    assert 'font-size="14.0"' in svg
    assert 'stroke="blue"' in svg


def test_dimension_markers():
    d = Dimension(0, 0, 100, 0)
    markers = d.get_markers()
    assert len(markers) == 2
    assert (
        "ArrowMarker-context-stroke-none-None-1-False-auto-start-reverse-point"
        in markers[0].id
    )
    assert "ArrowMarker-context-stroke-none-None-1-False-auto-point" in markers[1].id


def test_dimension_with_negative_offset():
    d = Dimension(0, 0, 100, 0, offset=-15)
    svg = d.to_svg()
    assert "<g>" in svg
    assert '<line x1="0.0" y1="15.0" x2="100.0" y2="15.0" ' in svg
    assert '<line x1="0.0" y1="0.0" x2="0.0" y2="19.0"' in svg
    assert '<text x="0" y="0"' in svg
    assert "translate(50.0, 13.0)" in svg
