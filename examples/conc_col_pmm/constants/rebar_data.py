REBAR_SIZES = ["#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#14", "#18"]
REBAR_DIAMETERS = [0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 1.13, 1.27, 1.41, 1.69, 2.26]
REBAR_AREAS = [0.11, 0.20, 0.31, 0.44, 0.60, 0.79, 1.00, 1.27, 1.56, 2.25, 4.00]
STEEL_E = 29000  # steel modulus of elasticity in ksi
REBAR_STRENGTHS = ["40 ksi", "60 ksi", "80 ksi"]
fy_dict = {"40 ksi": 40, "60 ksi": 60, "80 ksi": 80}


def rebar_area(size):
    for pos, name in enumerate(REBAR_SIZES):
        if size == name:
            return REBAR_AREAS[pos]
    raise Exception("invalid rebar size")


def rebar_diameter(size):
    for pos, name in enumerate(REBAR_SIZES):
        if size == name:
            return REBAR_DIAMETERS[pos]
    raise Exception("invalid rebar size")
