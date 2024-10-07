import math

from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits
from examples.conc_col_pmm.struct_analysis.try_axis import try_axis

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

    (lambda1, ecc, pn, phi_pn_not_limited, phi_mn_xy) = try_axis(
        example_col2, -43.9 * math.pi / 180, 12.5, axial_limits
    )
    phi_pn = min(axial_limits.max_phi_pn, phi_pn_not_limited)

    found = (
        phi_pn,
        phi_mn_xy * math.cos(lambda1),
        phi_mn_xy * math.sin(lambda1),
    )
    for i in range(3):
        ref = reference_forces[i]
        assert abs((found[i] - ref) / ref) < tol
