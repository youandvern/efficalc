import dataclasses

from numpy import ndarray

from ...pmm_search.load_combo import LoadCombination


@dataclasses.dataclass
class PMM:
    X: ndarray
    Y: ndarray
    Z: ndarray
    load_combos: list[LoadCombination]
