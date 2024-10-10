import dataclasses


@dataclasses.dataclass
class LoadCombination:
    p: float
    mx: float
    my: float
    show_in_report: bool


def is_yes(show: str):
    return show.strip().lower() == "yes" or show.strip().lower() == "y"
