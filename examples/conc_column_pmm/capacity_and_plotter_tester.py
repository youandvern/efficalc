import sections
import pmm_plotter
import get_capacity
import point_plotter
import get_dcr_ecc

column1 = sections.Column(40, 40, "#7", 1.5, 8, 9, 9330, 80, False, False)

mesh = pmm_plotter.plot(column1, 36, 12, False)

# define a load with Mx, My, and then P, all ultimate
load = [200, -100, 400]

capacity_pts = get_capacity.get_capacity(mesh, load)

# plot the PM diagram for this point
point_plotter.plot(capacity_pts, load)

# print("the DCR is", get_dcr.get_dcr(capacity_pts, load))

print("the DCR is", get_dcr_ecc.get_dcr(column1, load))
