import dataclasses


@dataclasses.dataclass
class LoadCombination:
    p: float
    mx: float
    my: float
    show_in_report: bool
