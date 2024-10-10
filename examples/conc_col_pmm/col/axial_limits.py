import dataclasses

from efficalc import Calculation


@dataclasses.dataclass
class AxialLimits:
    max_pn: float
    max_phi_pn: float
    max_phi_pn_calculation: Calculation
    min_pn: float
    min_phi_pn: float

    # difference between the maximum and minimum allowable loads,
    # to be used for normalizing error
    @property
    def load_span(self) -> float:
        return self.max_phi_pn - self.min_phi_pn
