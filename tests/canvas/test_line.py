from efficalc.canvas import Line, Marker


class TestMarker(Marker):
    def __init__(self, test_id, **kwargs):
        self.test_id = test_id
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.test_id


def test_line_defaults():
    l = Line(1, 2, 3, 4)
    svg = l.to_svg()
    assert "<line " in svg
    assert 'x1="1"' in svg
    assert 'y1="2"' in svg
    assert 'x2="3"' in svg
    assert 'y2="4"' in svg
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg
    assert "marker-start" not in svg
    assert "marker-end" not in svg
    assert " />" in svg
    assert l.get_markers() == []


def test_line_with_markers():
    l = Line(
        1,
        2,
        3,
        4,
        marker_start=TestMarker("test-start"),
        marker_end=TestMarker("test-end"),
    )
    svg = l.to_svg()
    assert ' marker-start="url(#test-start)" ' in svg
    assert ' marker-end="url(#test-end)" ' in svg
    assert l.get_markers() == [TestMarker("test-start"), TestMarker("test-end")]


def test_line_custom_style():
    l = Line(1, 2, 3, 4, fill="red", stroke="blue", stroke_width=5)
    svg = l.to_svg()
    assert "<line " in svg
    assert 'x1="1"' in svg
    assert 'y1="2"' in svg
    assert 'x2="3"' in svg
    assert 'y2="4"' in svg
    assert 'fill="red"' in svg
    assert 'stroke="blue"' in svg
    assert 'stroke-width="5"' in svg
    assert "marker-start" not in svg
    assert "marker-end" not in svg
    assert " />" in svg
