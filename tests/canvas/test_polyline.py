import re

import pytest

from efficalc.canvas import Marker, Polyline


@pytest.fixture
def points_with_all_combinations():
    # Set up a points array with all combinations of (clockwise, counterclockwise), (obtuse, acute, right) angles
    yield [
        (0, 0),
        (30, 10),
        (60, 10),
        (60, 30),
        (30, 30),
        (30, 50),
        (60, 50),
        (20, 60),
        (70, 70),
        (100, 100),
    ]  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test


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


def test_path_all_corners_filleted(points_with_all_combinations):
    p = Polyline(
        points_with_all_combinations,
        corner_radius=2,
    )
    expected_path = "M 0,0 L 29.692099788303082,9.897366596101028 A 2,2 0 0,0 30.32455532033676,10.0 L 58.0,10.0 A 2,2 0 0,1 60.0,12.0 L 60.0,28.0 A 2,2 0 0,1 58.0,30.0 L 32.0,30.0 A 2,2 0 0,0 30.0,32.0 L 30.0,48.0 A 2,2 0 0,0 32.0,50.0 L 43.753788748764684,50.0 A 2,2 0 0,1 44.23885999883735,53.940285000290665 L 28.62861901269609,57.84284524682597 A 2,2 0 0,0 28.72145799249239,61.74429159849848 L 69.40620812114003,69.88124162422801 A 2,2 0 0,1 70.42818941323675,70.42818941323675 L 100,100"
    assert_same_paths(expected_path, p.to_path_commands())


def test_path_some_corners_not_able_to_fillet(points_with_all_combinations):
    p = Polyline(
        points_with_all_combinations,
        corner_radius=8,
    )
    expected_path = "M 0,0 L 28.768399153212332,9.58946638440411 A 8,8 0 0,0 31.298221281347036,10.0 L 52.0,10.0 A 8,8 0 0,1 60.0,18.0 L 60.0,22.0 A 8,8 0 0,1 52.0,30.0 L 38.0,30.0 A 8,8 0 0,0 30.0,38.0 L 30.0,42.0 A 8,8 0 0,0 38.0,50.0 L 60,50 L 54.514476050784374,51.37138098730391 A 8,8 0 0,0 54.885831969969566,66.97716639399391 L 67.62483248456009,69.52496649691201 A 8,8 0 0,1 71.712757652947,71.712757652947 L 100,100"
    assert_same_paths(expected_path, p.to_path_commands())


def test_path_all_corners_not_able_to_fillet(points_with_all_combinations):
    p = Polyline(
        points_with_all_combinations,
        corner_radius=500,
    )
    expected_path = "M 0,0 L 30,10 L 60,10 L 60,30 L 30,30 L 30,50 L 60,50 L 20,60 L 70,70 L 100,100"
    actual_path = p.to_path_commands()
    assert "A" not in actual_path
    assert_same_paths(expected_path, actual_path)


def test_path_no_fillet(points_with_all_combinations):
    p = Polyline(
        points_with_all_combinations,
        corner_radius=0,
    )
    expected_path = "M 0,0 30,10 60,10 60,30 30,30 30,50 60,50 20,60 70,70 100,100"
    actual_path = p.to_path_commands()
    assert "A" not in actual_path
    assert_same_paths(expected_path, actual_path)


def test_path_semi_circle_without_straight_segment():
    p = Polyline(
        [(50, 25), (75, 25), (75, 75), (25, 75), (25, 50)],
        corner_radius=25,
    )
    expected_path = "M 50,25 L 50.0,25.0 A 25,25 0 0,1 75.0,50.0 L 75.0,50.0 A 25,25 0 0,1 50.0,75.0 L 50.0,75.0 A 25,25 0 0,1 25.0,50.0 L 25,50"
    assert_same_paths(expected_path, p.to_path_commands())


def test_svg_includes_markers():
    p = Polyline(
        [(0, 0), (10, 10)],
        corner_radius=25,
        marker_start=TestMarker("test-start"),
        marker_end=TestMarker("test-end"),
        marker_mid=TestMarker("test-mid"),
    )
    expected_path = "M 0,0 L 10,10"
    assert p.to_path_commands() == expected_path

    svg = p.to_svg()
    assert f'd="{expected_path}"' in svg
    assert ' marker-start="url(#test-start)" ' in svg
    assert ' marker-end="url(#test-end)" ' in svg
    assert ' marker-mid="url(#test-mid)" ' in svg


def test_svg_no_markers_when_none():
    p = Polyline(
        [(0, 0), (10, 10)],
        corner_radius=25,
    )
    expected_path = "M 0,0 L 10,10"
    assert p.to_path_commands() == expected_path

    svg = p.to_svg()
    assert f'd="{expected_path}"' in svg
    assert "marker-start" not in svg
    assert "marker-end" not in svg
    assert "marker-mid" not in svg


def test_common_style_elements_not_requested():
    p = Polyline([(0, 0), (10, 10)])
    assert p.get_common_svg_style_elements() == ""
    svg = p.to_svg()
    assert "fill" not in svg
    assert "stroke" not in svg
    assert "stroke-width" not in svg


def test_common_style_elements_requested():
    p = Polyline([(0, 0), (10, 10)], fill="red", stroke="blue", stroke_width=5)
    assert (
        p.get_common_svg_style_elements()
        == ' fill="red" stroke="blue" stroke-width="5"'
    )
    svg = p.to_svg()
    assert ' fill="red" ' in svg
    assert ' stroke="blue" ' in svg
    assert ' stroke-width="5" ' in svg
