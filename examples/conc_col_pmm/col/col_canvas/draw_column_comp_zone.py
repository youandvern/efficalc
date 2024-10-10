import math

from efficalc.canvas import Canvas, Dimension, Polyline, Rectangle, Text

from ..column import Column
from .draw_plain_column import draw as draw_base


def draw(col: Column, caption_input: str, points) -> Canvas:
    # number is the zone number with which to label this triangle, points are the three
    # corners of the triangle as a tuple of 2-element tuples
    canvas = draw_base(col)
    canvas.caption = caption_input

    points = [(pt[0] + col.w / 2, col.h / 2 - pt[1]) for pt in points]
    n = len(points)
    centr = [sum((points[i][j] for i in range(n))) / n for j in range(2)]
    points.append(points[0])

    canvas.add(Polyline(points, stroke_width=0.2, stroke="#c80c00"))

    canvas.add(
        Rectangle(
            centr[0] - 0.3,
            centr[1] - 1,
            10,
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
            "Compression Zone",
            centr[0],
            centr[1],
            font_size=1.2,
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
    for pt in points[:-1]:
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
