from efficalc import FigureFromMatplotlib, Heading
from examples.conc_col_pmm.calc_document.plotting import point_plotter

"""
This function plots the intersection of the PMM surface with the vertical planes
Mx-P and My-P. 
"""


def plot(mesh):
    Heading("PM Diagrams for Pure Mx and My")
    n = len(mesh)
    m = len(mesh[0])
    capacity_pts = [
        [mesh[i][0][0] for i in range(n)],
        [mesh[i][0][2] for i in range(n)],
    ]
    pm_figure = point_plotter.plot(capacity_pts, None, True)
    FigureFromMatplotlib(pm_figure, "PM interaction diagram for pure Mx.")

    capacity_pts = [
        [mesh[i][m - 1][1] for i in range(n)],
        [mesh[i][m - 1][2] for i in range(n)],
    ]
    pm_figure = point_plotter.plot(capacity_pts, None, False)
    FigureFromMatplotlib(pm_figure, "PM interaction diagram for pure My.")
