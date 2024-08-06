import pytest

from efficalc import (
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
)
from efficalc.canvas import Canvas, CircleMarker, Line, Marker


@pytest.fixture
def common_setup_teardown():
    yield None
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


# Helper class to create a unique test marker
class TestMarker(Marker):
    def __init__(self, test_id, **kwargs):
        self.test_id = test_id
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.test_id

    def to_svg(self) -> str:
        return f"svg-{self.id}"


def test_save_calc_item(common_setup_teardown):
    c = Canvas(10, 10)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == c


def test_canvas_defaults_no_elements(common_setup_teardown):
    c = Canvas(5, 5)
    assert (
        '<svg viewbox="0 0 5 5" style="max-width: 100%; display: block; width: 5.0px; margin-inline: auto;" xmlns="http://www.w3.org/2000/svg">\n \n </svg>'
        == c.to_svg()
    )


def test_canvas_with_shifted_viewbox(common_setup_teardown):
    c = Canvas(5, 5, min_xy=(-5, 100.2))
    assert (
        '<svg viewbox="-5 100.2 5 5" style="max-width: 100%; display: block; width: 5.0px; margin-inline: auto;" xmlns="http://www.w3.org/2000/svg">\n \n </svg>'
        == c.to_svg()
    )


def test_canvas_with_one_element(common_setup_teardown):
    c = Canvas(5, 5)
    c.add(Line(0, 0, 5, 5))
    svg = c.to_svg()
    assert "<svg " in svg
    assert " </svg>" in svg
    assert '<line x1="0" y1="0" x2="5" y2="5"' in svg
    assert "/>" in svg


def test_multiple_elements(common_setup_teardown):
    canvas = Canvas(width=200, height=100)
    line1 = Line(0, 0, 100, 100)
    line2 = Line(100, 100, 200, 0)
    canvas.add(line1)
    canvas.add(line2)
    svg = canvas.to_svg()
    assert "<svg " in svg
    assert " </svg>" in svg
    assert '<line x1="0" y1="0" x2="100" y2="100"' in svg
    assert '<line x1="100" y1="100" x2="200" y2="0"' in svg


def test_canvas_styling_properties(common_setup_teardown):
    canvas = Canvas(
        width=300,
        height=200,
        background_color="lightgrey",
        border_width=2,
        border_color="black",
        centered=False,
        full_width=True,
    )
    svg = canvas.to_svg()
    assert (
        'style="max-width: 100%; display: block; width: 100%; background-color: lightgrey; border: 2px solid black;'
        in svg
    )


def test_canvas_scale_property(common_setup_teardown):
    canvas = Canvas(width=300, height=200, scale=2)
    svg = canvas.to_svg()
    assert 'style="max-width: 100%; display: block; width: 600px;' in svg


def test_centered_and_full_width(common_setup_teardown):
    canvas = Canvas(width=200, height=100, centered=True, full_width=True)
    svg = canvas.to_svg()
    assert (
        'style="max-width: 100%; display: block; width: 100%; margin-inline: auto;'
        in svg
    )


def test_to_svg_does_not_mutate_elements(common_setup_teardown):
    marker = CircleMarker(fill="context-fill")
    line = Line(0, 0, 100, 100, fill="banana", marker_start=marker)
    canvas = Canvas(width=200, height=100)
    canvas.add(line)
    svg = canvas.to_svg()
    assert 'marker-start="url(#CircleMarker-banana-' in svg
    assert '<circle cx="1.0" cy="1.0" r="1" fill="banana"' in svg
    assert "context-fill" not in svg
    assert marker.fill == "context-fill"


def test_default_props_applied_to_sub_element(common_setup_teardown):
    canvas = Canvas(
        width=200, height=100, default_element_fill="blue", default_element_stroke="red"
    )
    line = Line(0, 0, 100, 100, stroke_width=2)
    canvas.add(line)
    svg = canvas.to_svg()
    assert (
        '<line x1="0" y1="0" x2="100" y2="100" fill="blue" stroke="red" stroke-width="2"'
        in svg
    )


def test_default_props_not_applied_when_sub_element_has_props(common_setup_teardown):
    canvas = Canvas(
        width=200, height=100, default_element_fill="blue", default_element_stroke="red"
    )
    line = Line(0, 100, 100, 0, fill="yellow", stroke="green")
    canvas.add(line)
    svg = canvas.to_svg()
    assert (
        '<line x1="0" y1="100" x2="100" y2="0" fill="yellow" stroke="green" stroke-width="1"'
        in svg
    )


def test_unique_markers_are_only_added_once(common_setup_teardown):
    marker = TestMarker("unique-marker")
    line1 = Line(0, 0, 100, 100, marker_start=marker)
    line2 = Line(100, 100, 200, 0, marker_end=marker)
    canvas = Canvas(width=200, height=100)
    canvas.add(line1)
    canvas.add(line2)
    svg = canvas.to_svg()
    assert svg.count(marker.to_svg()) == 1
    assert svg.count("url(#unique-marker)") == 2


def test_different_context_fill_markers_from_same_origin_marker(common_setup_teardown):
    marker = CircleMarker(fill="context-fill")
    line1 = Line(0, 0, 100, 100, marker_start=marker, fill="red")
    line2 = Line(100, 100, 200, 0, marker_start=marker, fill="blue")
    canvas = Canvas(width=200, height=100)
    canvas.add(line1)
    canvas.add(line2)
    svg = canvas.to_svg()
    assert svg.count('marker-start="url(#CircleMarker-red-') == 1
    assert svg.count('marker-start="url(#CircleMarker-blue-') == 1
    assert '<circle cx="1.0" cy="1.0" r="1" fill="red"' in svg
    assert '<circle cx="1.0" cy="1.0" r="1" fill="blue"' in svg
    assert "context-fill" not in svg
    assert marker.fill == "context-fill"
