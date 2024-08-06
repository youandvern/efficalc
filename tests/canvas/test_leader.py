import re

import pytest

from efficalc.canvas import Leader, Marker


class TestMarker(Marker):
    def __init__(self, test_id, **kwargs):
        self.test_id = test_id
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.test_id


def assert_same_paths(expected_path, actual_path):
    expected = re.split(r"[ ,]", expected_path)
    actual = re.split(r"[ ,]", actual_path)
    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        try:
            a_num = float(a)
            e_num = float(e)
            assert a_num == pytest.approx(
                e_num
            ), f"Numbers {a_num} and {e_num} are not approximately equal"
        except ValueError:
            assert a == e, f"Strings do not match: {a} != {e}"


def test_leader_defaults():
    l = Leader(0, 0, 50, 50, text="Leader Text")
    svg = l.to_svg()
    assert "<g>" in svg
    assert_same_paths("M 48,50 43,50 0,0", l._get_leader_line().to_path_commands())
    assert '<path d="M 48,50 43,50 0,0" fill="none" stroke-width="1" ' in svg
    assert '<text x="0" y="0" ' in svg
    assert 'transform="translate(50, 50) rotate(0)" ' in svg
    assert 'font-size="7.0" stroke="none" stroke-width="0" ' in svg
    assert 'dominant-baseline="middle"' in svg
    assert "marker-end" not in svg


def test_leader_with_marker():
    marker = TestMarker("test-marker_leader")
    l = Leader(0, 0, 50, 50, text="Leader Text", marker=marker)
    svg = l.to_svg()

    assert "<g>" in svg
    assert 'marker-end="url(#test-marker_leader)"' in svg
    assert '<text x="0" y="0" ' in svg
    assert 'transform="translate(50, 50) rotate(0)" ' in svg


def test_leader_with_custom_style():
    l = Leader(0, 0, 50, 50, text="Leader Text", stroke="blue", stroke_width=2)
    svg = l.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="2"' in svg
    assert 'fill="none"' in svg
    assert 'stroke="blue"' in svg
    assert '<text x="0" y="0" ' in svg
    assert 'font-size="14.0" fill="blue" stroke="none" stroke-width="0" ' in svg


def test_leader_with_landing_len():
    l = Leader(0, 0, 50, 50, text="Leader Text", landing_len=10)
    svg = l.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert_same_paths("M 48,50 38,50 0,0", l._get_leader_line().to_path_commands())
    assert '<text x="0" y="0" ' in svg
    assert 'transform="translate(50, 50) rotate(0)" ' in svg
    assert 'font-size="7.0" stroke="none" stroke-width="0" ' in svg


def test_leader_with_left_direction():
    l = Leader(0, 0, 50, 50, text="Leader Text", direction="left")
    svg = l.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert_same_paths("M 52,50 57,50 0,0", l._get_leader_line().to_path_commands())
    assert '<text x="0" y="0" ' in svg
    assert 'transform="translate(50, 50) rotate(0)" ' in svg
    assert 'font-size="7.0" stroke="none" stroke-width="0" ' in svg


def test_leader_text_size():
    l = Leader(0, 0, 50, 50, text="Leader Text", text_size=2)
    svg = l.to_svg()
    assert "<g>" in svg
    assert 'stroke-width="1"' in svg
    assert_same_paths("M 48,50 43,50 0,0", l._get_leader_line().to_path_commands())
    assert '<text x="0" y="0" ' in svg
    assert 'transform="translate(50, 50) rotate(0)" ' in svg
    assert 'font-size="14" stroke="none" stroke-width="0" ' in svg
