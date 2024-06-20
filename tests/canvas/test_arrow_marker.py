from efficalc.canvas import ArrowMarker


def test_arrow_marker_id_with_defaults():
    m = ArrowMarker()
    assert m.id == "ArrowMarker-context-stroke-none-None-1-False-auto"


def test_arrow_marker_id_with_some_customization():
    m = ArrowMarker(orientation="auto-start-reverse", fill="blue")
    assert m.id == "ArrowMarker-blue-none-None-1-False-auto-start-reverse"


def test_arrow_marker_id_with_full_customization():
    m = ArrowMarker(
        reverse=True, orientation=30, fill="red", stroke="blue", stroke_width=5, size=3
    )
    assert m.id == "ArrowMarker-red-blue-5-3-True-30"


def test_svg_style_props_default():
    m = ArrowMarker()
    svg = m.to_svg()

    assert m.id in svg
    assert f'orient="auto"' in svg
    assert f'markerUnits="strokeWidth"' in svg
    assert 'fill="context-stroke"' in svg
    assert 'stroke="none"' in svg
    assert "stroke-width" not in svg
    assert "<marker " in svg
    assert "<path " in svg
    assert " />" in svg
    assert "</marker>" in svg


def test_svg_style_props_custom():
    m = ArrowMarker(orientation=30, fill="red", stroke="blue", stroke_width=5)
    svg = m.to_svg()

    assert m.id in svg
    assert f'orient="30"' in svg
    assert f'markerUnits="strokeWidth"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert "<marker " in svg
    assert "<path " in svg
    assert " />" in svg
    assert "</marker>" in svg


def test_svg_size_props_without_stroke():
    m = ArrowMarker()
    svg = m.to_svg()
    assert m.stroke_width is None
    assert m.size == 1
    stroke_width = 0
    marker_size = 4
    middle = marker_size / 2

    assert f'viewBox="0 0 {marker_size} {marker_size}"' in svg
    assert f'refX="{middle}"' in svg
    assert f'refY="{middle}"' in svg
    assert f'markerWidth="{marker_size}"' in svg
    assert f'markerHeight="{marker_size}"' in svg
    assert (
        f'd="M {stroke_width} {stroke_width} L {marker_size} {middle} L {stroke_width} {marker_size} z"'
        in svg
    )


def test_svg_size_props_with_stroke():
    m = ArrowMarker(stroke="blue", stroke_width=5)
    svg = m.to_svg()
    assert m.stroke_width == 5
    assert m.size == 1
    stroke_width = 5
    marker_size = 4
    middle = marker_size / 2 + stroke_width

    assert (
        f'viewBox="0 0 {marker_size+2*stroke_width} {marker_size+2*stroke_width}"'
        in svg
    )
    assert f'refX="{middle}"' in svg
    assert f'refY="{middle}"' in svg
    assert f'markerWidth="{marker_size+2*stroke_width}"' in svg
    assert f'markerHeight="{marker_size+2*stroke_width}"' in svg
    assert (
        f'd="M {stroke_width} {stroke_width} L {marker_size+stroke_width} {middle} L {stroke_width} {marker_size+stroke_width} z"'
        in svg
    )


def test_svg_size_props_with_stroke_and_scale():
    m = ArrowMarker(stroke="blue", stroke_width=5, size=5)
    svg = m.to_svg()
    assert m.stroke_width == 5
    assert m.size == 5
    stroke_width = 5
    marker_size = 20
    middle = marker_size / 2 + stroke_width

    assert (
        f'viewBox="0 0 {marker_size+2*stroke_width} {marker_size+2*stroke_width}"'
        in svg
    )
    assert f'refX="{middle}"' in svg
    assert f'refY="{middle}"' in svg
    assert f'markerWidth="{marker_size+2*stroke_width}"' in svg
    assert f'markerHeight="{marker_size+2*stroke_width}"' in svg
    assert (
        f'd="M {stroke_width} {stroke_width} L {marker_size+stroke_width} {middle} L {stroke_width} {marker_size+stroke_width} z"'
        in svg
    )


def test_svg_reverse():
    m = ArrowMarker(reverse=True)
    svg = m.to_svg()
    assert 'viewBox="0 0 4 4"' in svg
    assert 'd="M 0 2.0 L 4 0 L 4 4 z"' in svg
    assert 'orient="auto"' in svg
