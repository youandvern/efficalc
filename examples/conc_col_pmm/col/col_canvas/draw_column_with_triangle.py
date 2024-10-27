import math

from efficalc.canvas import Canvas, CircleMarker, Dimension, Polyline, Rectangle, Text

from ...struct_analysis import triangles
from ..column import Column
from .draw_plain_column import draw as draw_base


def draw(col: Column, caption_input: str, number, points) -> Canvas:
    # number is the zone number with which to label this triangle, points are the three
    # corners of the triangle as a tuple of 2-element tuples
    canvas = draw_base(col)
    canvas.caption = caption_input

    points = [(pt[0] + col.w / 2, col.h / 2 - pt[1]) for pt in points]
    points.append(points[0])

    marker = CircleMarker()
    canvas.add(
        Polyline(
            points,
            stroke_width=0.2,
            stroke="#c80c00",
            marker_mid=marker,
            marker_end=marker,
        )
    )

    centr = triangles.triangle_centroid(*points[:3])
    canvas.add(
        Rectangle(
            centr[0] - 0.3,
            centr[1] - 1,
            3.8,
            1.4,
            0.2,
            0.2,
            stroke_width=0.12,
            stroke="#c80c00",
            fill="white",
        )
    )
    canvas.add(
        Text(
            "Area " + str(number),
            centr[0],
            centr[1],
            font_size=1.2,
        )
    )

    pt_labels = ["Point A", "Point B", "Point C"]
    for i in range(3):
        offsets = (
            [0.2] * 2
            if (points[i][0] > 1e-6 and points[i][1] < col.h - 1e-6)
            else [-3, -1.1]
        )
        canvas.add(
            Text(
                pt_labels[i],
                points[i][0] + offsets[0],
                points[i][1] - offsets[1],
                font_size=1,
            )
        )

    # margin around the section
    m = 8
    scale_factor = 0.37817187 * math.log((col.w + col.h) / 2) + 0.03808133
    # add dimensions
    common_dim_styles = {
        "unit": '"',
        "gap": 0.15,
        "stroke_width": 0.08 * scale_factor,
        "text_size": 1.2,
    }
    for pt in points:
        if pt[0] == 0 and 0 < pt[1] < col.h:
            # this point is on the left edge, add dimension
            canvas.add(Dimension(0, 0, 0, pt[1], offset=-0.5 * m, **common_dim_styles))
        if pt[0] == col.w and 0 < pt[1] < col.h:
            # this point is on the right edge, add dimension
            canvas.add(
                Dimension(col.w, 0, col.w, pt[1], offset=0.5 * m, **common_dim_styles)
            )
        if pt[1] == 0 and 0 < pt[0] < col.w:
            # this point is on the top edge, add dimension
            canvas.add(
                Dimension(col.w, 0, pt[0], 0, offset=0.5 * m, **common_dim_styles)
            )
        if pt[1] == col.h and 0 < pt[0] < col.w:
            # this point is on the bottom edge, add dimension
            canvas.add(
                Dimension(
                    col.w, col.h, pt[0], col.h, offset=-0.5 * m, **common_dim_styles
                )
            )
    return canvas
