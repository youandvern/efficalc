import sections
import pmm_plotter

column1 = sections.Column(20, 30, "#8", 1.5, 3, 5, 8000, 60, False, False)

pmm_plotter.plot(column1, 32, 10, True)
