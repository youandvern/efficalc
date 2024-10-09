from ..struct_analysis.triangles import *

tri1 = ((0, 0), (3, 0), (0, 6))


def test_triangle_area():
    assert triangle_area(tri1[0], tri1[1], tri1[2]) == 9


def test_triangle_centroid():
    assert triangle_centroid(tri1[0], tri1[1], tri1[2]) == (1, 2)
