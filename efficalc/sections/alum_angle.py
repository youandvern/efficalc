import dataclasses


@dataclasses.dataclass
class AluminumAngle(object):
    """This is a dataclass containing the properties of an Aluminium Angle section.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param Iz: Moment of inertia about the z-axis (in^4)
    :type Iz: float
    :param R1: Fillet radius (in)
    :type R1: float
    :param R2: Tip radius (in)
    :type R2: float
    :param Size: The section size name
    :type Size: str
    :param Sx: Elastic section modulus about the x-axis (in^3)
    :type Sx: float
    :param Sy: Elastic section modulus about the y-axis (in^3)
    :type Sy: float
    :param Type: The type of section shape (e.g. American Standard, Aluminum Association, etc.)
    :type Type: str
    :param W: Nominal weight (lb/ft)
    :type W: float
    :param alpha: Angle of the z-axis (deg)
    :type alpha: float
    :param b: Width (in)
    :type b: float
    :param d: Depth (in)
    :type d: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param rz: Radius of gyration about the z-axis (in)
    :type rz: float
    :param t: Thickness (in)
    :type t: float
    :param x: Location of the centroid along the x-axis (in)
    :type x: float
    :param y: Location of the centroid along the y-axis (in)
    :type y: float
    """

    A: float
    Ix: float
    Iy: float
    Iz: float
    R1: float
    R2: float
    Size: str
    Sx: float
    Sy: float
    Type: str
    W: float
    alpha: float
    b: float
    d: float
    rx: float
    ry: float
    rz: float
    t: float
    x: float
    y: float


ALL_ALUMINUM_ANGLE_NAMES = (
    "L 1 1/2 x 1 1/2 x 1/8",
    "L 1 3/4 x 1 3/4 x 1/8",
    "L 1 3/4 x 1 3/4 x 1/4",
    "L 1 1/2 x 1 1/2 x 1/4",
    "L 2 x 2 x 1/8",
    "L 1 3/4 x 1 3/4 x 3/8",
    "L 2 x 2 x 3/16",
    "L 2 x 2 x 1/4",
    "L 2 x 2 x 3/8",
    "L 2 x 2 x 5/16",
    "L 2 1/2 x 2 1/2 x 1/8",
    "L 2 1/2 x 2 1/2 x 3/16",
    "L 2 1/2 x 2 1/2 x 1/4",
    "L 2 1/2 x 2 1/2 x 5/16",
    "L 2 1/2 x 2 1/2 x 3/8",
    "L 2 1/2 x 2 1/2 x 1/2",
    "L 3 x 3 x 3/16",
    "L 3 x 3 x 1/4",
    "L 3 x 3 x 5/16",
    "L 3 x 3 x 3/8",
    "L 3 x 3 x 1/2",
    "L 3 1/2 x 3 1/2 x 1/4",
    "L 3 1/2 x 3 1/2 x 5/16",
    "L 3 1/2 x 3 1/2 x 3/8",
    "L 3 1/2 x 3 1/2 x 1/2",
    "L 4 x 4 x 1/4",
    "L 4 x 4 x 5/16",
    "L 4 x 4 x 3/8",
    "L 4 x 4 x 1/2",
    "L 4 x 4 x 7/16",
    "L 4 x 4 x 5/8",
    "L 4 x 4 x 9/16",
    "L 5 x 5 x 3/8",
    "L 4 x 4 x 11/16",
    "L 4 x 4 x 3/4",
    "L 5 x 5 x 9/16",
    "L 5 x 5 x 7/16",
    "L 5 x 5 x 1/2",
    "L 5 x 5 x 3/4",
    "L 5 x 5 x 5/8",
    "L 6 x 6 x 7/16",
    "L 8 x 8 x 1/2",
    "L 6 x 6 x 3/8",
    "L 6 x 6 x 1/2",
    "L 1 3/4 x 1 1/4 x 1/8",
    "L 8 x 8 x 1",
    "L 6 x 6 x 5/8",
    "L 6 x 6 x 3/4",
    "L 8 x 8 x 5/8",
    "L 2 x 1 1/4 x 1/8",
    "L 1 3/4 x 1 1/4 x 1/4",
    "L 2 x 1 x 3/16",
    "L 1 3/4 x 1 1/4 x 3/16",
    "L 2 x 1 1/4 x 1/4",
    "L 2 x 1 1/2 x 1/8",
    "L 2 x 1 1/2 x 1/4",
    "L 2 x 1 1/2 x 3/16",
    "L 2 x 1 1/2 x 3/8",
    "L 8 x 8 x 3/4",
    "L 2 x 1 3/4 x 1/4",
    "L 2 1/4 x 1 1/2 x 1/4",
    "L 2 1/2 x 1 1/4 x 1/8",
    "L 2 1/2 x 1 1/2 x 1/8",
    "L 2 1/2 x 1 1/2 x 3/16",
    "L 2 1/2 x 1 1/2 x 1/4",
    "L 2 1/2 x 1 1/2 x 5/16",
    "L 2 1/2 x 1 1/2 x 3/8",
    "L 2 1/2 x 2 x 1/8",
    "L 2 1/2 x 2 x 1/4",
    "L 2 1/2 x 2 x 3/16",
    "L 2 1/2 x 2 x 5/16",
    "L 2 1/2 x 2 x 3/8",
    "L 3 x 1 1/2 x 1/4",
    "L 3 x 2 x 3/16",
    "L 3 x 2 x 1/4",
    "L 3 x 2 x 5/16",
    "L 3 x 2 x 3/8",
    "L 3 x 2 x 1/2",
    "L 3 x 2 1/2 x 1/4",
    "L 3 x 2 1/2 x 5/16",
    "L 3 x 2 1/2 x 3/8",
    "L 3 1/2 x 3 x 1/4",
    "L 3 1/2 x 3 x 5/16",
    "L 3 1/2 x 3 x 3/8",
    "L 3 1/2 x 3 x 1/2",
    "L 4 x 3 x 1/4",
    "L 4 x 3 x 3/8",
    "L 4 x 3 x 5/16",
    "L 4 x 3 1/2 x 5/16",
    "L 4 x 3 x 5/8",
    "L 4 x 3 x 1/2",
    "L 4 x 3 x 7/16",
    "L 5 x 3 x 3/8",
    "L 4 x 3 1/2 x 3/8",
    "5 x 3 1/2 x 5/16",
    "L 4 x 3 1/2 x 1/2",
    "L 5 x 3 x 1/2",
    "L 5 x 3 x 1/4",
    "5 x 3 1/2 x 1/2",
    "L 5 x 3 x 5/16",
    "5 x 3 1/2 x 3/8",
    "5 x 3 1/2 x 5/8",
    "6 x 3 x 3/8",
    "6 x 3 1/2 x 5/16",
    "6 x 3 1/2 x 3/8",
    "6 x 3 1/2 x 5/8",
    "6 x 3 1/2 x 1/2",
    "6 x 4 x 3/8",
    "6 x 4 x 5/8",
    "7 x 4 x 1/2",
    "6 x 4 x 7/16",
    "6 x 4 x 3/4",
    "6 x 4 x 1/2",
    "8 x 6 x 5/8",
    "8 x 6 x 11/16",
    "8 x 6 x 3/4",
)
