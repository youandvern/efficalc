import math

from examples.conc_col_pmm.col.assign_max_min import calculate_axial_load_limits
from examples.conc_col_pmm.pmm_search.ecc_search.point_search_ecc import search

search_tol = 1.5e-3  # the tolerance for error in the points found
ceil_tol = 1e-2  # how close to limits to go

"""
The function below chooses an arbitrary initial guess and then
for a range of target points (where the target lambda and load
are both allowed to vary) checks whether the eccentricity search
algorithm converges. 
"""


def test_search(example_col):
    axial_limits = calculate_axial_load_limits(example_col)
    guess = [-0.7, 30]
    lambda_change = math.pi / 12
    ecc_change = math.pi / 12
    lambda_target = 0
    while lambda_target < math.pi / 2 - ceil_tol:
        ecc_target = -math.pi / 2 + ecc_change
        while ecc_target < math.pi / 2 - ceil_tol:
            target = [lambda_target, ecc_target]
            Mx, My, P, guess = search(example_col, target, guess, axial_limits)
            lambda_found = math.atan2(My, Mx)
            Mxy_found = math.sqrt(Mx**2 + My**2)
            ecc_found = math.atan2(P, Mxy_found)
            assert abs(lambda_found - lambda_target) < search_tol
            assert abs(ecc_found - ecc_target) < search_tol
            ecc_target += ecc_change
        lambda_target += lambda_change
