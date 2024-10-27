import dataclasses


@dataclasses.dataclass
class LoadCombination:
    id: int
    p: float
    mx: float
    my: float
    show_in_report: bool


def is_yes(show: str | float):
    trimmed_yes = f"{show}".strip().lower()
    return trimmed_yes == "yes" or trimmed_yes == "y"
