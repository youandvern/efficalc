import dataclasses


@dataclasses.dataclass
class AluminumChannel(object):
    """
    This is a dataclass containing the properties of an Aluminum Channel section.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
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
    :param b: Width (in)
    :type b: float
    :param d: Depth (in)
    :type d: float
    :param d1: Nominal depth between flange fillets (in)
    :type d1: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param tf: Average flange thickness (in)
    :type tf: float
    :param tftip: Flange thickness at the tip (in)
    :type tftip: float
    :param tw: Thickness of the web (in)
    :type tw: float
    """

    A: float
    Ix: float
    Iy: float
    R1: float
    R2: float
    Size: str
    Sx: float
    Sy: float
    Type: str
    W: float
    b: float
    d: float
    d1: float
    rx: float
    ry: float
    tf: float
    tftip: float
    tw: float
    x: float


ALL_ALUMINUM_CHANNEL_NAMES = (
    "CS 2 X 1.07",
    "CS 2 X 0.577",
    "CS 3 X 1.60",
    "CS 4 X 1.74",
    "CS 4 X 2.33",
    "CS 5 X 3.09",
    "CS 5 X 2.21",
    "CS 6 X 4.03",
    "CS 6 X 2.83",
    "CS 7 X 4.72",
    "CS 7 X 3.21",
    "CS 8 X 5.79",
    "CS 8 X 4.15",
    "CS 10 X 6.14",
    "CS 9 X 6.97",
    "CS 9 X 4.98",
    "CS 12 X 8.27",
    "CS 10 X 8.36",
    "CS 14 X 13.91",
    "CS 12 X 11.8",
    "C 3 X 1.42",
    "C 2 X 1.22",
    "CS 3 X 1.14",
    "C 3 X 1.73",
    "C 3 X 2.07",
    "C 4 X 1.85",
    "C 4 X 2.16",
    "C 5 X 2.32",
    "C 4 X 2.50",
    "C 5 X 3.11",
    "C 5 X 3.97",
    "C 6 X 2.83",
    "C 6 X 3.00",
    "C 6 X 3.63",
    "C 6 X 4.50",
    "C 8 X 4.25",
    "C 10 X 5.28",
    "C 7 X 3.54",
    "C 10 X 8.64",
    "C 10 X 10.4",
    "C 12 X 7.41",
    "C 7 X 5.10",
    "C 12 X 8.64",
    "C 12 X 10.4",
    "C 12 X 12.1",
    "C 15 X 11.7",
    "C 7 X 4.23",
    "C 7 X 5.96",
    "C 8 X 4.75",
    "C 9 X 6.91",
    "C 9 X 8.65",
    "C 8 X 5.62",
    "C 9 X 4.60",
    "C 9 X 5.19",
    "C 8 X 6.48",
    "C 10 X 6.91",
    "C 15 X 17.3",
)
