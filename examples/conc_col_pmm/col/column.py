from efficalc import Calculation, Input

from ..constants.rebar_data import STEEL_E, rebar_area, rebar_diameter

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
    rebar_area = area of one longitudinal bar (in^2)
    steel_modulus = steel modulus of elasticity (ksi)
    concrete_strain = max concrete strain at f'c
"""


class Column:
    # a constant for now
    shear_bar_size = "#4"

    def __init__(
        self,
        w_input: Input,
        h_input: Input,
        bar_size_input: Input,
        bar_cover_input: Input,
        bars_x_input: Input,
        bars_y_input: Input,
        fc_input: Input,
        fy_input: Input,
        cover_to_center: bool,
        spiral_reinf: bool,
        rebar_area_input: Calculation,
        steel_modulus_input: Calculation,
        concrete_strain_input: Calculation,
    ):

        self.w_input = w_input
        self.h_input = h_input
        self.bar_size_input = bar_size_input
        self.bar_cover_input = bar_cover_input
        self.bars_x_input = bars_x_input
        self.bars_y_input = bars_y_input
        self.fc_input = fc_input
        self.fy_input = fy_input
        self.rebar_area_input = rebar_area_input
        self.steel_modulus_input = steel_modulus_input
        self.concrete_strain_input = concrete_strain_input

        self.cover_to_center = cover_to_center
        self.spiral_reinf = spiral_reinf

        self.w = w_input.get_value()
        self.h = h_input.get_value()
        self.bar_size = bar_size_input.get_value()
        self.bar_cover = bar_cover_input.get_value()
        self.bars_x = bars_x_input.get_value()
        self.bars_y = bars_y_input.get_value()
        self.fc = fc_input.get_value()
        self.fy = fy_input.get_value()

        self.half_w = self.w / 2
        self.half_h = self.h / 2
        self.area = self.w * self.h

        # coordinates of three corner points
        self.bot_right = (self.half_w, -self.half_h)
        self.top_right = (self.half_w, self.half_h)
        self.top_left = (-self.half_w, self.half_h)

        self.bar_area = rebar_area(self.bar_size)
        self.bar_dia = rebar_diameter(self.bar_size)
        if cover_to_center:  # the concrete cover is to center of bars
            self.edge_to_bar_center = self.bar_cover
        else:
            self.edge_to_bar_center = self.bar_cover + self.bar_dia / 2

        # the center-to-center spacing of the top/bottom bars
        self.x_space = (self.w - 2 * self.edge_to_bar_center) / (self.bars_x - 1)

        # the center-to-center spacing of the left/right bars
        self.y_space = (self.h - 2 * self.edge_to_bar_center) / (self.bars_y - 1)

        # the y-coordinate of the bottom left corner bar
        self.y_start = -self.half_h + self.edge_to_bar_center

        # the x-coordinate of the second-from-left bar on the bottom edge
        self.x_start = -self.half_w + self.edge_to_bar_center + self.x_space

        self.beta1 = max(
            0.65, min(0.85, 0.85 - 0.05 / 1000 * (self.fc - 4000))
        )  # the ratio
        # of a/c for this column
        self.steel_yield = self.fy / STEEL_E  # strain in steel at yielding

        # safety factor for compression-controlled column
        self.PHI_COMP = 0.75 if spiral_reinf else 0.65
