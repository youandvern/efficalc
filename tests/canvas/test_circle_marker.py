from efficalc.canvas import CircleMarker


def test_circle_marker_id_with_defaults():
    marker = CircleMarker()
    assert marker.id == "CircleMarker-context-stroke-none-None-1"


def test_circle_marker_id_with_some_customization():
    marker = CircleMarker(fill="blue")
    assert marker.id == "CircleMarker-blue-none-None-1"


def test_circle_marker_id_with_full_customization():
    marker = CircleMarker(fill="red", stroke="blue", stroke_width=5, size=3)
    assert marker.id == "CircleMarker-red-blue-5-3"


def test_svg_style_props_default():
    marker = CircleMarker()
    svg = marker.to_svg()

    assert "<marker" in svg
    assert 'id="' + marker.id in svg
    assert f'markerUnits="strokeWidth"' in svg
    assert 'fill="context-stroke"' in svg
    assert 'stroke="none"' in svg
    assert "stroke-width" not in svg
    assert "<marker " in svg
    assert "<circle " in svg
    assert " />" in svg
    assert "</marker>" in svg


def test_svg_style_props_custom():
    marker = CircleMarker(fill="red", stroke="blue", stroke_width=5)
    svg = marker.to_svg()

    assert 'id="' + marker.id in svg
    assert f'markerUnits="strokeWidth"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert "<marker " in svg
    assert "<circle " in svg
    assert " />" in svg
    assert "</marker>" in svg


def test_svg_size_props_without_stroke():
    marker = CircleMarker()
    svg = marker.to_svg()
    assert marker.stroke_width is None
    assert marker.size == 1
    radius = marker.size
    diameter = marker.size * 2

    assert f'viewBox="0 0 {diameter} {diameter}"' in svg
    assert f'refX="{float(radius)}"' in svg
    assert f'refY="{float(radius)}"' in svg
    assert f'markerWidth="{diameter}"' in svg
    assert f'markerHeight="{diameter}"' in svg
    assert f'cx="{float(radius)}"' in svg
    assert f'cy="{float(radius)}"' in svg
    assert f'r="{radius}"' in svg


def test_svg_size_props_with_stroke():
    marker = CircleMarker(stroke="blue", stroke_width=0.5)
    svg = marker.to_svg()
    assert marker.stroke_width == 0.5
    assert marker.size == 1
    radius = marker.size
    diameter = marker.size * 2
    stroke_width = marker.stroke_width

    view_size = diameter + stroke_width
    middle = view_size / 2

    assert f'viewBox="0 0 {view_size} {view_size}"' in svg
    assert f'refX="{middle}"' in svg
    assert f'refY="{middle}"' in svg
    assert f'markerWidth="{view_size}"' in svg
    assert f'markerHeight="{view_size}"' in svg
    assert f'cx="{middle}"' in svg
    assert f'cy="{middle}"' in svg
    assert f'r="{radius}"' in svg
    assert f'stroke-width="{stroke_width}"' in svg


def test_svg_size_props_with_stroke_and_size():
    marker = CircleMarker(stroke="blue", stroke_width=2, size=5)
    svg = marker.to_svg()
    assert marker.stroke_width == 2
    assert marker.size == 5
    radius = marker.size
    diameter = marker.size * 2
    stroke_width = marker.stroke_width

    view_size = diameter + stroke_width
    middle = view_size / 2

    assert f'viewBox="0 0 {view_size} {view_size}"' in svg
    assert f'refX="{middle}"' in svg
    assert f'refY="{middle}"' in svg
    assert f'markerWidth="{view_size}"' in svg
    assert f'markerHeight="{view_size}"' in svg
    assert f'cx="{middle}"' in svg
    assert f'cy="{middle}"' in svg
    assert f'r="{radius}"' in svg
    assert f'stroke-width="{stroke_width}"' in svg
