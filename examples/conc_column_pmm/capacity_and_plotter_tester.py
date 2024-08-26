import sections
import pmm_plotter
import get_capacity
import point_plotter
import get_dcr_ecc
import max_tens_comp

col = sections.Column(40, 40, "#7", 1.5, 8, 9, 9330, 80, False, False)

# max compression and tension capacity
(
    col.max_pn,
    col.max_phi_pn,
    col.min_pn,
    col.min_phi_pn,
    col.efficalc_inputs,
) = max_tens_comp.calculation(col)

col.load_span = col.max_phi_pn - col.min_phi_pn  # difference between the
# maximum and minimum allowable loads, to be used for normalizing error

mesh = pmm_plotter.plot(col, 36, 12, False)

# define a load with Mx, My, and then P, all ultimate
load = [200, -100, 400]

capacity_pts = get_capacity.get_capacity(mesh, load)

# plot the PM diagram for this point
point_plotter.plot(capacity_pts, load)

# print("the DCR is", get_dcr.get_dcr(capacity_pts, load))

print("the DCR is", get_dcr_ecc.get_dcr(col, load))
