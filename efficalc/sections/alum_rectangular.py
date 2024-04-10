import dataclasses


@dataclasses.dataclass
class AluminumRectangular(object):
    """This is a dataclass containing the properties of an Aluminum Rectangular section, typically representing
    rectangular HSS (Hollow Structural Section) properties.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param J: Torsional constant (in^4)
    :type J: float
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
    :param Zx: Plastic section modulus about the x-axis (in^4)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^4)
    :type Zy: float
    :param b: Width (in)
    :type b: float
    :param d: Depth (in)
    :type d: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param t: Thickness (in)
    :type t: float
    """

    A: float
    Ix: float
    Iy: float
    J: float
    Size: str
    Sx: float
    Sy: float
    Type: str
    W: float
    Zx: float
    Zy: float
    b: float
    d: float
    rx: float
    ry: float
    t: float


ALL_ALUMINUM_RECTANGULAR_NAMES = (
    "RT 1 x 1 x 0.065",
    "RT 1 x 1 x 0.125",
    "RT 1.25 x 1.25 x 0.065",
    "RT 1 x 1 x 0.0 95",
    "RT 1.25 x 1.25 x  0.095",
    "RT 1.25 x 1.25 x 0.125",
    "RT 1.5 x 1.5 x 0.065",
    "RT 1.375 x 1.375 x 0.125",
    "RT 1.5 x 1.5 x 0.095",
    "RT 1.5 x 1.5 x 0.078",
    "RT 1.5 x 1.5 x 0.125",
    "RT 1.5 x 1.5 x 0.25",
    "RT 2 x 2 x 0.095",
    "RT 2 x 2 x 0.125",
    "RT 2 x 2 x 0.156",
    "RT 2 x 2 x 0.25",
    "RT 2.25 x 2.25 x 0.125",
    "RT 2.5 x 2.5 x 0.125",
    "RT 2.5 x 2.5 x 0.188",
    "RT 2.5 x 2.5 x 0.25",
    "RT 2.75 x 2.75 x 0.188",
    "RT 2.75 x 2.75 x 0.125",
    "RT 3 x 3 x 0.125",
    "RT 3 x 3 x 0.095",
    "RT 2 x 2 x 0.188",
    "RT 3 x 3 x 0.188",
    "RT 3 x 3 x 0.25",
    "RT 3.5 x 3.5 x 0.125",
    "RT 3 x 3 x 0.375",
    "RT 3.5 x 3.5 x 0.25",
    "RT 3.5 x 3.5 x 0.375",
    "RT 4 x 4 x 0.125",
    "RT 4 x 4 x 0.188",
    "RT 4 x 4 x 0.25",
    "RT 4 x 4 x 0.5",
    "RT 4 x 4 x 0.375",
    "RT 1.75 x 1.75 x 0.125",
    "RT 5 x 5 x 0.125",
    "RT 5 x 5 x 0.188",
    "RT 5 x 5 x 0.25",
    "RT 5 x 5 x 0.375",
    "RT 6 x 6 x 0.188",
    "RT 6 x 6 x 0.125",
    "RT 6 x 6 x 0.25",
    "RT 6 x 6 x 0.5",
    "RT 8 x 8 x 0.188",
    "RT 8 x 8 x 0.25",
    "RT 8 x 8 x 0.375",
    "RT 8 x 8 x 0.5",
    "RT 1 1/2 x 1 x 1/8",
    "RT 1 3/4 x 1 1/2 x 1/8",
    "RT 2 x 1 x 1/8",
    "RT 2 x 1 1/4  x 1/8",
    "RT 2 x 1 1/2 x 1/8",
    "RT 2 x 1 1/2 x 1/4",
    "RT 2 x 1 3/4 x 1/8",
    "RT 2 1/4 x 1 3/4 x 1/8",
    "RT 2 1/2 x 1 x 1/8",
    "RT 2 1/2 x 1 1/4 x 1/8",
    "RT 2 1/2 x 1 1/2 x 1/8",
    "RT 6 x 6 x 0.375",
    "RT 2 1/2 x 1 3/4 x 1/8",
    "RT 2 3/4 x 1 3/4 x 1/8",
    "RT 3 x 1 x 1/8",
    "RT 3 x 1 1/4 x 1/8",
    "RT 3 x 1 1/2 x 1/8",
    "RT 3 x 1 1/2 x 3/16",
    "RT 3 x 1 3/4 x 1/8",
    "RT 3 x 2 x 1 /8",
    "RT 3 x 2 x 1/4",
    "RT 3 1/2 x 1 3/4 x 1/8",
    "RT 4 x 1 x 1/8",
    "RT 4 x 1 1/2 x 1/8",
    "RT 4 x 1 3/4 x 1/8",
    "RT 4 x 2 x 3/16",
    "RT 4 x 3 x 3/16",
    "RT 4 x 2 x 1/4",
    "RT 4 x 2 1/2 x 1/8",
    "RT 4 x 2 x 1/8",
    "RT 5 x 2 1/2 x 1/8",
    "RT 5 x 3 x 1/8",
    "RT 5 x 3 x 3/16",
    "RT 4 1/2 x 1 3/4 x 1/8",
    "RT 4 x 3 x 1/8",
    "RT 4 x 3 x 1/4",
    "RT 4 x 3 x 1/2",
    "RT 4 x 3 x 3/8",
    "RT 5 x 2 x 3/16",
    "RT 5 x 3 x 1/4",
    "RT 5 x 1 3/4 x 1/8",
    "RT 5 x 2 x 1/4",
    "RT 5 x 2 x 1/8",
    "RT 6 x 1 1/2 x 1/8",
    "RT 6 x 1 3/4 x 1/8",
    "RT 5 x 1 3/4 x 3/  16",
    "RT 5 x 4 x 1/4",
    "RT 6 x 2 x 3/16",
    "RT 6 x 2 x 1/4",
    "RT 6 x 3 x 3/16",
    "RT 6 x 4 x 1/8",
    "RT 6 x 3 x 1/8",
    "RT 6 x 4 x 3/16",
    "RT 6 x 4 x 1/4",
    "RT 6 x 4 x 1/2",
    "RT 8 x 2 x 1/8",
    "RT 8 x 4 x 3/16",
    "RT 8 x 3 x 1/4",
    "RT 8 x 4 x 3/8",
    "RT 8 x 4 x 1/4",
    "RT 8 x 4 x 1/2",
    "RT 6 x 2 x 1/8",
    "RT 8 x 5 x 3/8",
)
