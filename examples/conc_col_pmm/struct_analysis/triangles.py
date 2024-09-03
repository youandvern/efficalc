def triangle_area(pt_a, pt_b, pt_c):
    return 0.5 * abs(
        pt_a[0] * pt_b[1]
        + pt_b[0] * pt_c[1]
        + pt_c[0] * pt_a[1]
        - pt_a[0] * pt_c[1]
        - pt_b[0] * pt_a[1]
        - pt_c[0] * pt_b[1]
    )


def triangle_centroid(pt_a, pt_b, pt_c):
    return ((pt_a[0] + pt_b[0] + pt_c[0]) / 3, (pt_a[1] + pt_b[1] + pt_c[1]) / 3)
