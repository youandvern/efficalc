import sections
import pmm_plotter
import get_capacity
import point_plotter
import get_dcr

column1=sections.Column(40,40,"#7",1.5,8,9,9330,80,False,False)

column1=sections.Column(16,30,"#8",1.5,3,3,4000,60,False,False)

mesh=pmm_plotter.plot(column1,36,12, False)

# define a load with Mx, My, and then P, all ultimate
load=[100,14.054083470239146,100]

load=[100,8.748866352592401,100]

load=[100,100,0]



capacity_pts=get_capacity.get_capacity(mesh, load)

point_plotter.plot(capacity_pts, load)

print("the DCR is",get_dcr.get_dcr(capacity_pts, load))