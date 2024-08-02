These functions can be used to find the axial load and biaxial moment capacity of 
reinforced concrete columns and to plot the PMM diagram. The function 'pmm_plotter'
plots the PMM diagram, the class 'Column' in sections.py defines a column section. 
'bisection_factored' is the function which searches for a given point on the PMM
diagram to achieve a particular neutral axis angle and axial load, and 'try_axis'
checks a certain neutral axis angle and depth. 

The following commands define an example column and plot the PMM diagram:

column1=sections.Column(20,30,"#8",1.5,3,5,8000,60,False,False)

pmm_plotter.plot(column1,32,10)