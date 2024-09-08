from examples.conc_col_pmm.constants.rebar_data import *

"""
The class Column takes the following parameters:
    w = section width (x-dir) (in.)
    h = section height (y-dir) (in.)
    bar_size = rebar number (Imperial)
    bar_cover = concrete cover to the longitudinal rebar (in.)
    bars_x = number of bars on the top/bottom edge
    bars_y = number of bars on the left/right edge
    fc = concrete f'c (psi)
    fy = steel yield strength (ksi)
    cover_to_center = boolean: concrete cover is to the center of the rebar,
        false means it is clear cover (to edge of bars)
    spiral_reinf = boolean: the shear reinforcement is spiral
"""


class Column:
    def __init__(
        self,
        w,
        h,
        bar_size,
        bar_cover,
        bars_x,
        bars_y,
        fc,
        fy,
        cover_to_center,
        spiral_reinf,
    ):
        self.w = w
        self.h = h
        self.half_w = w / 2
        self.half_h = h / 2
        self.area = w * h

        # coordinates of three corner points
        self.bot_right = (self.half_w, -self.half_h)
        self.top_right = (self.half_w, self.half_h)
        self.top_left = (-self.half_w, self.half_h)

        self.bar_size = bar_size
        self.bar_cover = bar_cover
        self.bar_area = rebar_area(bar_size)  # area of one bar in in^2
        self.bar_dia = rebar_diameter(bar_size)
        self.bars_x = bars_x
        self.bars_y = bars_y
        self.cover_to_center = cover_to_center
        if cover_to_center:  # the concrete cover is to center of bars
            self.edge_to_bar_center = bar_cover
        else:
            self.edge_to_bar_center = bar_cover + self.bar_dia / 2

        # the center-to-center spacing of the top/bottom bars
        self.x_space = (self.w - 2 * self.edge_to_bar_center) / (self.bars_x - 1)

        # the center-to-center spacing of the left/right bars
        self.y_space = (self.h - 2 * self.edge_to_bar_center) / (self.bars_y - 1)

        # the y-coordinate of the bottom left corner bar
        self.y_start = -self.half_h + self.edge_to_bar_center

        # the x-coordinate of the second-from-left bar on the bottom edge
        self.x_start = -self.half_w + self.edge_to_bar_center + self.x_space

        self.fc = fc
        self.beta1 = max(
            0.65, min(0.85, 0.85 - 0.05 / 1000 * (self.fc - 4000))
        )  # the ratio
        # of a/c for this column
        self.fy = fy
        self.steel_yield = self.fy / STEEL_E  # strain in steel at yielding

        self.spiral_reinf = spiral_reinf
        # safety factor for compression-controlled column
        self.PHI_COMP = 0.75 if spiral_reinf else 0.65