from efficalc.canvas import Canvas, Circle, Rectangle

from ...constants.rebar_data import rebar_diameter


def draw(col) -> Canvas:
    # margin around the section
    m = 8

    # define reinforcement properties
    bars_x = col.bars_x
    bars_y = col.bars_y
    long_bar_radius = rebar_diameter(col.bar_size) / 2
    stirrup_diameter = rebar_diameter(col.shear_bar_size)
    stirrup_bend_radius = 3 * stirrup_diameter

    # define "cover" to be the cover to center of bar (regardless of whether the user specified the
    # cover to be clear or to center)
    cover = col.bar_cover if col.cover_to_center else col.bar_cover + long_bar_radius

    # set up the canvas
    canvas = Canvas(
        col.w + 2 * m,
        col.h + 2 * m,
        min_xy=(-m, -m),
        scale=20,
        default_element_stroke_width=0,
    )

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

    return canvas
