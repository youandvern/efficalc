import dataclasses


@dataclasses.dataclass
class AiscAngle(object):
    """This is a dataclass containing the properties of an AISC Angle section. Properties follow the AISC shapes
    database.

    :param A: The section area (in^2)
    :type A: float
    :param AISC_name: The name of the AISC section
    :type AISC_name: str
    :param Cw: The warping constant (in^6)
    :type Cw: float
    :param EDI_Std_Nomenclature: The EDI standard nomenclature name
    :type EDI_Std_Nomenclature: str
    :param Iw: The moment of inertia about the w-axis (in^4)
    :type Iw: float
    :param Ix: The moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: The moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param Iz: The moment of inertia about the z-axis (in^4)
    :type Iz: float
    :param J: The torsional constant (in^4)
    :type J: float
    :param PA: The shape perimeter minus one flange surface (in)
    :type PA: float
    :param PA2: The single angle shape perimeter minus long leg surface (in)
    :type PA2: float
    :param PB: The shape perimeter for AISC Design Guide 19 (in)
    :type PB: float
    :param SwA: The elastic section modulus about the w-axis at point A (in^3)
    :type SwA: float
    :param SwB: The elastic section modulus about the w-axis at point B (in^3)
    :type SwB: float
    :param SwC: The elastic section modulus about the w-axis at point C (in^3)
    :type SwC: float
    :param Sx: The elastic section modulus about the x-axis (in^3)
    :type Sx: float
    :param Sy: The elastic section modulus about the y-axis (in^3)
    :type Sy: float
    :param Sz: The elastic section modulus about the z-axis (in^3)
    :type Sz: float
    :param SzA: The elastic section modulus about the z-axis at point A (in^3)
    :type SzA: float
    :param SzB: The elastic section modulus about the z-axis at point B (in^3)
    :type SzB: float
    :param SzC: The elastic section modulus about the z-axis at point C (in^3)
    :type SzC: float
    :param T_F: Whether the section has an additional note in the AISC shapes database (T or F)
    :type T_F: str
    :param Type: The section type
    :type Type: str
    :param W: The nominal section weight (lb/ft)
    :type W: float
    :param Zx: The plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: The plastic  section modulus about the y-axis (in^3)
    :type Zy: float
    :param b: The width of the longer angle leg (in)
    :type b: float
    :param b_t: The slenderness ratio, b/t
    :type b_t: float
    :param d: The width of the shorter leg (in)
    :type d: float
    :param kdes: Distance from outer face of flange to web toe of fillet used for design (in)
    :type kdes: float
    :param kdet: Distance from outer face of flange to web toe of fillet used for detailing (in)
    :type kdet: float
    :param ro: Polar radius of gyration about the shear center (in)
    :type ro: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param rz: Radius of gyration about the z-axis (in)
    :type rz: float
    :param t: Thickness of the angle leg (in)
    :type t: float
    :param tana: Tangent of the angle between the y-y and z-z axes for single angles
    :type tana: float
    :param wA: Distance from point A to center of gravity along the w-axis (in)
    :type wA: float
    :param wB: Distance from point B to center of gravity along the w-axis (in)
    :type wB: float
    :param wC: Distance from point C to center of gravity along the w-axis (in)
    :type wC: float
    :param x: Horizontal distance from designated edge of member to center of gravity of member (in)
    :type x: float
    :param xp: Horizontal distance from designated edge of member to plastic neutral axis of member (in)
    :type xp: float
    :param y: Vertical distance from designated edge of member to center of gravity of member (in)
    :type y: float
    :param yp: Vertical distance from designated edge of member to plastic neutral axis of member (in)
    :type yp: float
    :param zA: Distance from point A to center of gravity along the z-axis (in)
    :type zA: float
    :param zB: Distance from point B to center of gravity along the z-axis (in)
    :type zB: float
    :param zC: Distance from point C to center of gravity along the z-axis (in)
    :type zC: float
    """

    A: float
    AISC_name: str
    Cw: float
    EDI_Std_Nomenclature: str
    Iw: float
    Ix: float
    Iy: float
    Iz: float
    J: float
    PA: float
    PA2: float
    PB: float
    SwA: float
    SwB: float
    SwC: float
    Sx: float
    Sy: float
    Sz: float
    SzA: float
    SzB: float
    SzC: float
    T_F: str
    Type: str
    W: float
    Zx: float
    Zy: float
    b: float
    b_t: float
    d: float
    kdes: float
    kdet: float
    ro: float
    rx: float
    ry: float
    rz: float
    t: float
    tana: float
    wA: float
    wB: float
    wC: float
    x: float
    xp: float
    y: float
    yp: float
    zA: float
    zB: float
    zC: float


"""The names of all available AISC angle sections (AISC_name)"""
ALL_AISC_ANGLE_NAMES = (
    "L12X12X1-1/4",
    "L12X12X1-3/8",
    "L12X12X1-1/8",
    "L12X12X1",
    "L10X10X1-3/8",
    "L10X10X1-1/4",
    "L10X10X1-1/8",
    "L10X10X1",
    "L10X10X7/8",
    "L10X10X3/4",
    "L8X8X1-1/8",
    "L8X8X1",
    "L8X8X7/8",
    "L8X8X5/8",
    "L8X8X3/4",
    "L8X8X9/16",
    "L8X8X1/2",
    "L8X6X1",
    "L8X6X5/8",
    "L8X6X7/8",
    "L8X6X9/16",
    "L8X6X1/2",
    "L8X4X1",
    "L8X6X7/16",
    "L8X4X3/4",
    "L8X4X7/8",
    "L8X6X3/4",
    "L8X4X9/16",
    "L8X4X5/8",
    "L8X4X1/2",
    "L8X4X7/16",
    "L7X4X3/4",
    "L7X4X5/8",
    "L7X4X1/2",
    "L7X4X7/16",
    "L7X4X3/8",
    "L6X6X1",
    "L6X6X7/8",
    "L6X6X3/4",
    "L6X6X5/8",
    "L6X6X9/16",
    "L6X6X1/2",
    "L6X6X7/16",
    "L6X6X3/8",
    "L6X4X7/8",
    "L6X4X3/4",
    "L6X4X5/8",
    "L6X4X9/16",
    "L6X4X1/2",
    "L6X6X5/16",
    "L6X4X7/16",
    "L6X4X3/8",
    "L6X4X5/16",
    "L6X3-1/2X1/2",
    "L6X3-1/2X3/8",
    "L6X3-1/2X5/16",
    "L5X5X7/8",
    "L5X5X3/4",
    "L5X5X5/8",
    "L5X5X7/16",
    "L5X5X3/8",
    "L5X5X1/2",
    "L5X3-1/2X3/4",
    "L5X5X5/16",
    "L5X3-1/2X5/8",
    "L5X3-1/2X1/2",
    "L5X3-1/2X3/8",
    "L5X3-1/2X5/16",
    "L5X3-1/2X1/4",
    "L5X3X1/2",
    "L5X3X7/16",
    "L5X3X3/8",
    "L5X3X1/4",
    "L5X3X5/16",
    "L4X4X5/8",
    "L4X4X3/4",
    "L4X4X3/8",
    "L4X4X5/16",
    "L4X4X7/16",
    "L4X4X1/4",
    "L4X3-1/2X1/2",
    "L4X3-1/2X3/8",
    "L4X3-1/2X5/16",
    "L4X3-1/2X1/4",
    "L4X3X5/8",
    "L4X3X1/2",
    "L4X3X3/8",
    "L4X4X1/2",
    "L4X3X5/16",
    "L4X3X1/4",
    "L3-1/2X3-1/2X1/2",
    "L3-1/2X3-1/2X7/16",
    "L3-1/2X3-1/2X3/8",
    "L3-1/2X3-1/2X5/16",
    "L3-1/2X3-1/2X1/4",
    "L3-1/2X3X1/2",
    "L3-1/2X3X7/16",
    "L3-1/2X3X3/8",
    "L3-1/2X3X1/4",
    "L3-1/2X2-1/2X3/8",
    "L3-1/2X2-1/2X1/2",
    "L3-1/2X3X5/16",
    "L3-1/2X2-1/2X5/16",
    "L3-1/2X2-1/2X1/4",
    "L3X3X7/16",
    "L3X3X1/2",
    "L3X3X5/16",
    "L3X3X3/8",
    "L3X3X3/16",
    "L3X3X1/4",
    "L3X2-1/2X7/16",
    "L3X2-1/2X1/2",
    "L3X2-1/2X3/8",
    "L3X2-1/2X3/16",
    "L3X2-1/2X1/4",
    "L3X2X1/2",
    "L3X2X3/16",
    "L3X2X3/8",
    "L3X2-1/2X5/16",
    "L3X2X5/16",
    "L2-1/2X2-1/2X1/2",
    "L3X2X1/4",
    "L2-1/2X2-1/2X3/8",
    "L2-1/2X2-1/2X5/16",
    "L2-1/2X2-1/2X3/16",
    "L2-1/2X2-1/2X1/4",
    "L2-1/2X2X3/8",
    "L2-1/2X2X1/4",
    "L2-1/2X2X5/16",
    "L2-1/2X1-1/2X1/4",
    "L2-1/2X2X3/16",
    "L2-1/2X1-1/2X3/16",
    "L2X2X3/8",
    "L2X2X5/16",
    "L2X2X1/4",
    "L2X2X3/16",
    "L2X2X1/8",
)
