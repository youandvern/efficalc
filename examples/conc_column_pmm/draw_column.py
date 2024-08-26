import dataclasses
import math
from typing import Literal
import triangles

from efficalc.canvas import (
    ArrowMarker,
    Canvas,
    Circle,
    Dimension,
    Leader,
    Line,
    Rectangle,
    Text,
    Polyline,
    CircleMarker,
)

BarSize = Literal["#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#14", "#18"]
BAR_SIZES = ["#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#14", "#18"]
REBAR_DIAMETERS = [0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 1.13, 1.27, 1.41, 1.69, 2.26]
REBAR_AREAS = [0.11, 0.20, 0.31, 0.44, 0.60, 0.79, 1.00, 1.27, 1.56, 2.25, 4.00]


def bar_size_to_area(bar_size: BarSize) -> float:
    return REBAR_AREAS[BAR_SIZES.index(bar_size)]


def bar_size_to_diameter(bar_size: BarSize) -> float:
    return REBAR_DIAMETERS[BAR_SIZES.index(bar_size)]


@dataclasses.dataclass
class Column:
    w: float
    h: float
    bar_size: BarSize
    bar_cover: float
    bars_x: int
    bars_y: int
    shear_bar_size: BarSize = "#3"
    fc: float = 5000
    fy: float = 60
    cover_to_center: bool = False
    spiral_reinf: bool = False


def draw_column_with_triangle(
    col: Column, caption_input: str, number, points, unit: str = '"'
) -> Canvas:
    # number is the zone number with which to label this triangle, points are the three
    # corners of the triangle as a tuple of 2-element tuples
    canvas = draw_column_section(col, caption_input)
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
    return canvas


def draw_column_comp_zone(
    col: Column, caption_input: str, points, unit: str = '"'
) -> Canvas:
    # number is the zone number with which to label this triangle, points are the three
    # corners of the triangle as a tuple of 2-element tuples
    canvas = draw_column_section(col, caption_input)
    points = [(pt[0] + col.w / 2, col.h / 2 - pt[1]) for pt in points]
    print("points", points)
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
    return canvas


def draw_column_section(col: Column, caption_input: str, unit: str = '"') -> Canvas:
    # margin around the section
    m = 8
    scale_factor = 0.37817187 * math.log((col.w + col.h) / 2) + 0.03808133

    # define reinforcement properties
    bars_x = col.bars_x
    bars_y = col.bars_y
    long_bar_radius = bar_size_to_diameter(col.bar_size) / 2
    stirrup_diameter = bar_size_to_diameter(col.shear_bar_size)
    stirrup_bend_radius = 3 * stirrup_diameter

    # define "cover" to be the cover to center of bar (regardless of whether the user specified the
    # cover to be clear or to center)
    cover = col.bar_cover if col.cover_to_center else col.bar_cover + long_bar_radius

    # set up the canvas
    canvas = Canvas(
        col.w + 2 * m,
        col.h + 2 * m,
        min_xy=(-m, -m),
        caption=caption_input,
        scale=20,
        default_element_stroke_width=0,
    )

    # x and y axes
    canvas.add(
        Line(
            col.w / 2,
            col.h / 2,
            col.w + m / 4,
            col.h / 2,
            stroke="black",
            stroke_width=0.08,
            marker_end=ArrowMarker(),
        )
    )
    canvas.add(
        Line(
            col.w / 2,
            col.h / 2,
            col.w / 2,
            -m / 4,
            stroke="black",
            stroke_width=0.08,
            marker_end=ArrowMarker(),
        )
    )
    canvas.add(Text("x", col.w + m / 4 + 0.25, col.h / 2, font_size=1))
    canvas.add(Text("y", col.w / 2, -m / 4 - 0.25, font_size=1))

    # Draw the beam outline
    column_outline = Rectangle(0, 0, col.w, col.h, fill="rgb(0 0 0 / 30%)")
    canvas.add(column_outline)

    # add transverse reinforcement
    stirrups = Rectangle(
        cover - long_bar_radius - stirrup_diameter / 2,
        cover - long_bar_radius - stirrup_diameter / 2,
        col.w - 2 * cover + 2 * long_bar_radius + stirrup_diameter,
        col.h - 2 * cover + 2 * long_bar_radius + stirrup_diameter,
        rx=stirrup_bend_radius,
        ry=stirrup_bend_radius,
        stroke_width=stirrup_diameter,
        stroke="#004aad",
    )

    canvas.add(stirrups)

    # add longitudinal reinforcement
    x_bar_starting_x = cover
    x_bar_spacing = (col.w - 2 * cover) / (bars_x - 1)
    x_bar_y_bot = col.h - cover
    x_bar_y_top = x_bar_starting_x

    y_bar_starting_y = x_bar_starting_x
    y_bar_spacing = (col.h - 2 * cover) / (bars_y - 1)
    y_bar_x_left = x_bar_starting_x
    y_bar_x_right = col.w - cover

    for i in range(bars_x):
        # bottom bar
        canvas.add(
            Circle(
                x_bar_starting_x + i * x_bar_spacing,
                x_bar_y_bot,
                long_bar_radius,
                fill="black",
            )
        )

        # top bar
        canvas.add(
            Circle(
                x_bar_starting_x + i * x_bar_spacing,
                x_bar_y_top,
                long_bar_radius,
                fill="black",
            )
        )

    last_y_bar = bars_y - 1
    for i in range(bars_y):
        if i == 0 or i == last_y_bar:
            # corner bars are drawn as x bar
            pass

        # left bar
        canvas.add(
            Circle(
                y_bar_x_left,
                y_bar_starting_y + i * y_bar_spacing,
                long_bar_radius,
                fill="black",
            )
        )

        # right bar
        canvas.add(
            Circle(
                y_bar_x_right,
                y_bar_starting_y + i * y_bar_spacing,
                long_bar_radius,
                fill="black",
            )
        )

    # add dimensions
    common_dim_styles = {
        "unit": unit,
        "gap": 0.15,
        "stroke_width": 0.08 * scale_factor,
        "text_size": 1.2,
    }
    canvas.add(Dimension(0, 0, col.w, 0, offset=0.5 * m, **common_dim_styles))
    canvas.add(Dimension(col.w, 0, col.w, col.h, offset=0.5 * m, **common_dim_styles))
    canvas.add(
        Dimension(
            0,
            cover,
            col.bar_cover,
            cover,
            offset=0.25 * m + cover,
            **common_dim_styles,
        )
    )

    # add leaders
    common_leader_styles = {
        "marker": ArrowMarker(),
        "landing_len": 1,
        "stroke_width": 0.08 * scale_factor,
        "text_size": 1.2,
    }

    bottom_bar_x = x_bar_starting_x + (col.bars_x - 2) * x_bar_spacing
    bottom_bar_y = x_bar_y_bot
    canvas.add(
        Leader(
            bottom_bar_x + long_bar_radius * 0.85,
            bottom_bar_y + long_bar_radius * 0.85,
            bottom_bar_x + cover + m / 8,
            col.h + m / 8,
            f"({col.bars_x}){col.bar_size} x-direction, E.S.",
            **common_leader_styles,
        )
    )
    left_bar_x = y_bar_x_left + long_bar_radius * 0.85
    left_bar_y = (
        y_bar_starting_y + (col.bars_y - 2) * y_bar_spacing + long_bar_radius * 0.85
    )
    canvas.add(
        Leader(
            left_bar_x,
            left_bar_y,
            cover + 2 * long_bar_radius + x_bar_spacing,
            col.h + m / 5,
            f"({col.bars_y}){col.bar_size} y-direction, N.S.",
            **common_leader_styles,
        )
    )

    return canvas
