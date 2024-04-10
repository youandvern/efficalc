import dataclasses


@dataclasses.dataclass
class AluminumWideFlange(object):
    """This is a dataclass containing the properties of an Aluminum Wide Flange section.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param Cw: Warping constant (in^6)
    :type Cw: float
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param J: Torsional constant (in^4)
    :type J: float
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
    :param Zx: Plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^3)
    :type Zy: float
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
    :param tw: Thickness of the web (in)
    :type tw: float
    """

    A: float
    Cw: float
    Ix: float
    Iy: float
    J: float
    R1: float
    R2: float
    Size: str
    Sx: float
    Sy: float
    Type: str
    W: float
    Zx: float
    Zy: float
    b: float
    d: float
    d1: float
    rx: float
    ry: float
    tf: float
    tw: float


ALL_ALUMINUM_WIDE_FLANGE_NAMES = (
    "I 3 x 1.64",
    "I 10 x 10.3",
    "I 12 x 11.7",
    "I 12 x 14.3",
    "I 14 x 16.0",
    "I 6 x 4.03",
    "I 3 x 2.03",
    "WF 5 x 6.49",
    "WF 6 x 4.16",
    "WF 6 x 5.40",
    "WF 6 x 7.85",
    "WF 6 x 8.30",
    "WF 6 x 9.18",
    "WF 8 x 5.90",
    "WF 8 x 8.32",
    "WF 8 x 10.7",
    "WF 8 x 11.2",
    "WF 8 x 11.8",
    "I 5 x 3.70",
    "I 4 x 2.31",
    "I 8 x 7.02",
    "I 6 x 4.69",
    "I 7 x 5.80",
    "I 8 x 6.18",
    "I 10 x 8.65",
    "I 9 x 8.36",
    "WF 2 x 1.43",
    "WF 4 x 4.76",
    "I 4 x 2.79",
    "WF 8 x 13.0",
    "WF 10 x 11.4",
    "WF 10 x 7.30",
    "WF 12 x 13.8",
    "WF 12 x 18.3",
    "WF(A-N) 2 x 0.928",
    "WF(A-N) 3 x 0.769",
    "WF(A-N) 3 x 1.00",
    "WF(A-N) 4 x 1.14",
    "WF(A-N) 4 x 1.79",
    "WF(A-N) 4 x 2.35",
    "WF(A-N) 4 x 3.06",
    "WF(A-N) 4 x 4.14",
    "WF(A-N) 5 x 5.36",
    "S 4 x 3.28",
    "S 3 x 1.96",
    "S 4 x 2.64",
    "S 3 x 2.59",
    "S 6 x 4.30",
    "S 5 x 4.23",
    "S 5 x 3.43",
    "S 8 x 6.35",
    "S 6 x 5.10",
    "S 6 x 5.96",
    "S 5 x 5.10",
    "S 7 x 6.05",
    "S 8 x 8.81",
    "S 10 x 8.76",
    "S 9 x 7.51",
    "S 8 x 7.96",
    "S 12 x 11.0",
    "S 10 x 10.4",
    "S 10 x 12.1",
    "S 12 x 12.1",
    "S 12 x 14.1",
    "S 12 x 15.6",
    "S 12 x 17.3",
)
