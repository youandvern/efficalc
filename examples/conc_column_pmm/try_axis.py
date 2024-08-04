import math
import random
import triangles

STEEL_E = 29000  # steel modulus of elasticity in ksi
CONC_EPSILON = -0.003  # concrete strain at f'c
STEEL_ADD_STRAIN = 0.003  # steel strain at PHI_FLEXURE
PHI_FLEXURE = 0.9  # safety factor for flexure-controlled column
COMP_FACTOR = 0.8  # additional reduction factor for axial compression


def try_axis(col, theta, c):
    # this function returns the lambda, eccentricity, pn, phi_pn, and phi_mn
    # from particular neutral axis angle and neutral axis depth c. The neutral
    # axis angle must be between -90 degrees and 0 degrees, inclusive, and the
    # neutral axis depth must be greater than or equal to 0

    if c == 0:
        return (0, 0, col.min_pn, col.min_phi_pn, 0)
    a = col.beta1 * c
    epsilon = 1e-6  # acceptable error for considering the neutral axis to
    # be vertical or horizontal
    red_fc = 0.85 * col.fc / 1000  # reduced f'c for concrete compression limit, ksi
    pn = 0  # total axial force, kips (positive is compression)
    mn = [0, 0]  # Mnx, then Mny, kip-in (positive is compression to the right/top)

    intersects = [False] * 4  # whether line of concrete compression intersects the
    # left, top, right, and bottom edges of the section
    if theta > -math.pi / 2 + epsilon:
        left_y = col.half_h - a / math.cos(theta) - col.w * math.tan(theta)
        intersects[0] = -col.half_h < left_y < col.half_h

        right_y = col.half_h - a / math.cos(theta)
        intersects[2] = -col.half_h < right_y < col.half_h

    if theta < -epsilon:
        top_x = col.half_w + a / math.sin(theta)
        intersects[1] = -col.half_w < top_x < col.half_w

        # if theta is -90, take the tan of 0 and get a change
        # of zero, and if theta is -45, take the tan of 45
        # and get somewhat of an increase in x
        bot_x = col.half_w + a / math.sin(theta) + col.h * math.tan(math.pi / 2 + theta)
        intersects[3] = -col.half_w < bot_x < col.half_w

    if not any(intersects):  # the whole concrete section is in compression
        pn += red_fc * col.area
    else:

        def add_axial_moment(pt_a, pt_b, pt_c):
            nonlocal pn
            tri_area = triangles.triangle_area(pt_a, pt_b, pt_c)
            pn += tri_area * red_fc
            centr = triangles.triangle_centroid(pt_a, pt_b, pt_c)
            for i in range(2):
                mn[i] += tri_area * red_fc * centr[1 - i]

        pt1 = (-col.half_w, left_y) if intersects[0] else (top_x, col.half_h)
        pt2 = (bot_x, -col.half_h) if intersects[3] else (col.half_w, right_y)

        add_axial_moment(pt1, pt2, col.top_right)  # compression triangle to
        # top right corner
        if intersects[0]:  # there is a compression triangle to top left corner
            add_axial_moment(col.top_left, col.top_right, pt1)
        if intersects[3]:  # there is a compression triangle to bot right corner
            add_axial_moment(col.bot_right, col.top_right, pt2)

    strain_per_in = CONC_EPSILON / c
    steel_max_strain = 0  # value to keep record of greatest steel tensile strain

    # calculate a normal vector rotated 90 degrees from the neutral axis angle
    normal = (math.cos(theta + math.pi / 2), math.sin(theta + math.pi / 2))

    def add_bar(coords):
        nonlocal steel_max_strain
        nonlocal pn
        # "offset" is the distance from the center of the bar to the line
        # passing through the top right corner of the section and parallel to
        # the neutral axis
        offset = normal[0] * (col.half_w - coords[0]) + normal[1] * (
            col.half_h - coords[1]
        )
        strain = (c - offset) * strain_per_in
        steel_max_strain = max(steel_max_strain, strain)

        stress = strain * STEEL_E
        stress = max(-col.fy, min(col.fy, stress))
        if a > offset:
            # this means this bar is within the compression range,
            # so subtract the stress in the concrete, the stress
            # will be negative in this case, so add to it
            stress += red_fc
        # since negative strain and negative stress are defined as
        # compression for rebar but compression is positive in the conc.
        # the sign of everything needs to be changed
        force = col.bar_area * stress
        pn -= force
        for i in range(2):
            mn[i] -= force * coords[1 - i]

    right_bar_x = col.half_w - col.edge_to_bar_center  # x coordinate of bars on the
    # right edge
    y = col.y_start
    # iterate over the bars along the left and right lines
    # (this includes corner bars)
    for i in range(col.bars_y):
        for x in (-right_bar_x, right_bar_x):
            coords = (x, y)
            add_bar(coords)
        y += col.y_space

    top_bar_y = col.half_h - col.edge_to_bar_center  # y coordinate of bars on the
    # top edge
    x = col.x_start
    for i in range(col.bars_x - 2):
        # iterate over the bars along the top and bottom lines, and add the
        # force for each one
        for y in (-top_bar_y, top_bar_y):
            coords = (x, y)
            add_bar(coords)
        x += col.x_space

    lambda1 = math.atan2(mn[1], mn[0])  # atan2 takes y,x, and we want mny at top

    # if Mx and My are both zero, the angle isn't defined, so return a random
    # number to help avoid divide by zero errors
    if not any(mn):
        lambda1 = random.uniform(0, math.pi / 2)
    mn_xy = math.sqrt(mn[0] ** 2 + mn[1] ** 2) / 12  # the moment resultant in kip-ft
    ecc = mn_xy / pn  # the eccentricity in ft

    # calculate the factor of safety depending on the maximum steel strain
    phi = min(
        PHI_FLEXURE,
        max(
            col.PHI_COMP,
            col.PHI_COMP
            + (PHI_FLEXURE - col.PHI_COMP)
            * (steel_max_strain - col.steel_yield)
            / STEEL_ADD_STRAIN,
        ),
    )
    phi_pn = phi * pn
    phi_mn_xy = mn_xy * phi_pn / pn

    # returning the angle of eccentricity, the eccentricity in ft, the nominal
    # axial capacity in kip, the factored axial capacity in kip, and the
    # factored moment capacity in kip-ft
    return (lambda1, ecc, pn, phi_pn, phi_mn_xy)
