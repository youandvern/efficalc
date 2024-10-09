import math

from efficalc.canvas import ArrowMarker, Canvas, Dimension, Leader, Line, Text

from ...constants.rebar_data import rebar_diameter
from ..column import Column
from .draw_plain_column import draw as draw_base


def draw(col: Column, caption_input: str, unit: str = '"') -> Canvas:
    canvas = draw_base(col)
    canvas.caption = caption_input
    scale_factor = 0.37817187 * math.log((col.w + col.h) / 2) + 0.03808133

    # margin around the section
    m = 8

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

    # define reinforcement properties
    bars_x = col.bars_x
    bars_y = col.bars_y
    long_bar_radius = rebar_diameter(col.bar_size) / 2

    # define "cover" to be the cover to center of bar (regardless of whether the user specified the
    # cover to be clear or to center)
    cover = col.bar_cover if col.cover_to_center else col.bar_cover + long_bar_radius

    canvas.add(Text("x", col.w + m / 4 + 0.25, col.h / 2, font_size=1))
    canvas.add(Text("y", col.w / 2, -m / 4 - 0.25, font_size=1))

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

    x_bar_starting_x = cover
    x_bar_spacing = (col.w - 2 * cover) / (bars_x - 1)
    x_bar_y_bot = col.h - cover

    y_bar_starting_y = x_bar_starting_x
    y_bar_spacing = (col.h - 2 * cover) / (bars_y - 1)
    y_bar_x_left = x_bar_starting_x

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
