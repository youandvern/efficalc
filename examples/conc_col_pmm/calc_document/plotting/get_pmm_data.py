import numpy as np

from ...col.axial_limits import AxialLimits
from ...col.column import Column
from ...pmm_search.load_combo import LoadCombination
from .PMM import PMM
from .pmm_mesh import get_mesh

"""
This function takes inputs for a column and creates a
dataclass instance containing all the information for the 
PMM diagram for the given column. That information is used
for plotting the PMM diagram. 
"""


def get_pmm_data(
    col: Column,
    intervals: int,
    load_spaces: int,
    load_combos: list[LoadCombination],
    axial_limits: AxialLimits,
):
    # get the capacity point mesh for plotting the PMM surface. x, y,
    # and z correspond to Mx, My, and P, respectively. "quarter_mesh"
    # has just one quarter of the PMM mesh (including points aligned
    # with the x and y axes)
    x, y, z, _ = get_mesh(col, intervals, load_spaces, axial_limits)
    X = np.array(x)
    Y = np.array(y)
    Z = np.array(z)

    return PMM(X=X, Y=Y, Z=Z, load_combos=load_combos)
