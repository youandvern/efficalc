from ...pmm_search.load_combo import LoadCombination
import dataclasses


@dataclasses.dataclass
class PMM():
    X: list[float]
    Y: list[float]
    Z: list[float]
    load_combos: list[LoadCombination]