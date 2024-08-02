import sections
import pmm_plotter
import point_plotter

column1=sections.Column(20,15,"#7",1.5,3,5,8000,60,False,False)

mesh=pmm_plotter.plot(column1,32,10, False)

# define a load with Mx, My, and then P, all ultimate
load=[-200,100,500]

point_plotter.plot(mesh, load)