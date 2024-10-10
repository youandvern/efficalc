import math

from ..calc_document.try_axis_document import try_axis_document
from ..col.assign_max_min import calculate_axial_load_limits

# this test is based on the reference calculation by SP Column which can be found at the following link:
# https://structurepoint.org/publication/pdf/Biaxial-Bending-Interaction-Diagrams-for-Rectangular-Reinforced-Concrete-Column-Design-ACI-318-19.pdf
# page 11 of the page above indicates the values of theta and c being tried as well as the values
# for factored Mx, My, and P using the exact capacity method.

# The reference P, Mx, My are below, these are factored
reference_forces = (283.72, 214.29, 133.83)

# the error tolerance for this test
tol = 1e-3


def test_try_axis(example_col2):
    axial_limits = calculate_axial_load_limits(example_col2)
    (phi_mnx, phi_mny, phi_pn) = try_axis_document(
        example_col2, axial_limits, -43.9 * math.pi / 180, 12.5
    )
    found = (
        phi_pn.get_value(),
        phi_mnx.get_value(),
        phi_mny.get_value(),
    )
    print("found", found)
    for i in range(3):
        ref = reference_forces[i]
        assert abs((found[i] - ref) / ref) < tol
