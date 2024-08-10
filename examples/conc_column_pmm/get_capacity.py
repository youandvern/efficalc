import math


def get_capacity(mesh, point):
    pt_count = len(mesh)  # the number of rows of points vertically
    quarter = len(mesh[0]) - 1  # the number of angle spaces between points in a
    # quadrant

    angle_space = (math.pi / 2) / quarter  # the horizontal space between points

    lambda_transform = math.atan2(abs(point[1]), abs(point[0]))  # the angle for
    # the current point transformed to the range 0 to 90, where 0 must
    # correspond to My=0

    index = int(lambda_transform // angle_space)  # the position of the mesh point in
    # each row of "mesh" just below the lambda of the load point

    # if the point is at lambda=90, the point with the next lowest lambda
    # value must be used as "index"
    if index == quarter:
        index -= 1

    angle_extra = lambda_transform % angle_space

    # define factors that can be multiplied by the load values at two
    # adjacent points to interpolate between those points
    factors = [(angle_space - angle_extra) / angle_space, angle_extra / angle_space]

    phi_Mn = [0] * pt_count
    phi_Pn = [0] * pt_count

    for i in range(pt_count):
        # calculate the estimate of the biaxial moment and axial force capacity
        # at the current point
        phi_Pn[i] = sum((mesh[i][index + j][2] * factors[j] for j in range(2)))

        for j in range(2):
            moment = math.sqrt(sum((mesh[i][index + j][k] ** 2 for k in range(2))))
            phi_Mn[i] += moment * factors[j]
    return [phi_Mn, phi_Pn]
