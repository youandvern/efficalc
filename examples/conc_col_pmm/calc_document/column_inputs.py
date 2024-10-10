import dataclasses

from ..constants.rebar_data import REBAR_SIZES, REBAR_STRENGTHS


@dataclasses.dataclass
class ColumnInputs:
    w: float = 24
    h: float = 36
    bar_size: str = REBAR_SIZES[5]
    bar_cover: float = 2
    bars_x: int = 6
    bars_y: int = 8
    fc: float = 8000
    fy: float = REBAR_STRENGTHS[1]
    cover_to_center: bool = False
    spiral_reinf: bool = False
