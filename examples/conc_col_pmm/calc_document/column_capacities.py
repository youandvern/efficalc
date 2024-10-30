import dataclasses

from latexexpr_efficalc import Variable

from efficalc import Calculation


@dataclasses.dataclass
class ColumnCapacities:
    Mx: Calculation | Variable
    My: Calculation | Variable
    P: Calculation | Variable
