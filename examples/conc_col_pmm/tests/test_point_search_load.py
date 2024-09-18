from examples.conc_col_pmm.pmm_search.load_search.point_search_load import search
import math

search_tol = 1.5e-3  # the tolerance for error in the points found
ceil_tol = 1e-2  # how close to limits to go

"""
The function below chooses an arbitrary initial guess and then
for a range of target points (where the target lambda and load
are both allowed to vary) checks whether the load search
algorithm converges. 
"""


def test_search(example_col):
    guess = [-0.7, 30]
    lambda_change = math.pi / 12
    load_change = example_col.load_span / 10
    lambda_target = 0
    while lambda_target < math.pi / 2 - ceil_tol:
        load_target = example_col.min_phi_pn + load_change
        while load_target < example_col.max_phi_pn - ceil_tol:
            target = [lambda_target, load_target]
            Mx, My, P, _, _ = search(example_col, target, guess)
            lambda_found = math.atan2(My, Mx)
            assert abs(lambda_found - lambda_target) < search_tol
            assert (abs(P - load_target) / example_col.load_span) < search_tol
            load_target += load_change
        lambda_target += lambda_change
