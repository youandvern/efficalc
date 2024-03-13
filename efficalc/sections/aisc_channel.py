import dataclasses


@dataclasses.dataclass
class AiscChannel(object):
    """
    This is a dataclass containing the properties of an AISC Channel section. Properties follow the AISC shapes
    database.

    :param A: The cross-sectional area (in^2)
    :type A: float
    :param AISC_name: The name of the AISC section
    :type AISC_name: str
    :param Cw: The warping constant (in^6)
    :type Cw: float
    :param EDI_Std_Nomenclature: The EDI standard nomenclature name
    :type EDI_Std_Nomenclature: str
    :param H: Flexural constant
    :type H: float
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param J: Torsional constant (in^4)
    :type J: float
    :param PA: Shape perimeter minus one flange surface (in)
    :type PA: float
    :param PB: Shape perimeter, as used in AISC Design Guide 19 (in)
    :type PB: float
    :param PC: Box perimeter minus one flange surface, as used in Design Guide 19 (in)
    :type PC: float
    :param PD: Box perimeter, as used in AISC Design Guide 19 (in)
    :type PD: float
    :param Qf: Statical moment for a point in the flange directly above the vertical edge of the web (in^3)
    :type Qf: float
    :param Qw: Statical moment for a point at mid-depth of the cross section (in^3)
    :type Qw: float
    :param Sw1: Warping statical moment at point 1 on cross section (in^4)
    :type Sw1: float
    :param Sw2: Warping statical moment at point 2 on cross section (in^4)
    :type Sw2: float
    :param Sw3: Warping statical moment at point 3 on cross section (in^4)
    :type Sw3: float
    :param Sx: Elastic section modulus about the x-axis (in^3)
    :type Sx: float
    :param Sy: Elastic section modulus about the y-axis (in^3)
    :type Sy: float
    :param T: Distance between web toes of fillets at top and bottom of web (in)
    :type T: float
    :param T_F: Indicates if there is a special note for the shape (T or F)
    :type T_F: str
    :param Type: The section type
    :type Type: str
    :param W: Nominal weight (lb/ft)
    :type W: float
    :param WGi: The workable gage for the inner fastener holes in the flange (in)
    :type WGi: float
    :param Wno: Normalized warping function (in^2)
    :type Wno: float
    :param Zx: Plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^3)
    :type Zy: float
    :param bf: Width of flange (in)
    :type bf: float
    :param bfdet: Detailing value of flange width (in)
    :type bfdet: float
    :param b_t: Slenderness ratio for angles and channel flange, b/t
    :type b_t: float
    :param d: Overall depth of member (in)
    :type d: float
    :param ddet: Detailing value of member depth (in)
    :type ddet: float
    :param eo: Horizontal distance to shear center of member (in)
    :type eo: float
    :param h_tw: Slenderness ratio for web, h/tw
    :type h_tw: float
    :param ho: Distance between the flange centroids (in)
    :type ho: float
    :param kdes: Distance from outer face of flange to web toe of fillet for design (in)
    :type kdes: float
    :param kdet: Distance from outer face of flange to web toe of fillet for detailing (in)
    :type kdet: float
    :param ro: Polar radius of gyration about the shear center (in)
    :type ro: float
    :param rts: Effective radius of gyration (in)
    :type rts: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param tf: Thickness of flange (in)
    :type tf: float
    :param tfdet: Detailing value of flange thickness (in)
    :type tfdet: float
    :param tw: Thickness of web (in)
    :type tw: float
    :param twdet: Detailing value of web thickness (in)
    :type twdet: float
    :param twdet_2: Detailing value of twdet/2 (in)
    :type twdet_2: float
    :param x: Horizontal distance to center of gravity of member (in)
    :type x: float
    :param xp: Horizontal distance to plastic neutral axis of member (in)
    :type xp: float
    """

    A: float
    AISC_name: str
    Cw: float
    EDI_Std_Nomenclature: str
    H: float
    Ix: float
    Iy: float
    J: float
    PA: float
    PB: float
    PC: float
    PD: float
    Qf: float
    Qw: float
    Sw1: float
    Sw2: float
    Sw3: float
    Sx: float
    Sy: float
    T: float
    T_F: str
    Type: str
    W: float
    WGi: float
    Wno: float
    Zx: float
    Zy: float
    bf: float
    bfdet: float
    b_t: float
    d: float
    ddet: float
    eo: float
    h_tw: float
    ho: float
    kdes: float
    kdet: float
    ro: float
    rts: float
    rx: float
    ry: float
    tf: float
    tfdet: float
    tw: float
    twdet: float
    twdet_2: float
    x: float
    xp: float


ALL_AISC_CHANNEL_NAMES = (
    "C15X40",
    "C15X33.9",
    "C15X50",
    "C12X30",
    "C12X25",
    "C12X20.7",
    "C10X30",
    "C10X25",
    "C10X20",
    "C10X15.3",
    "C9X20",
    "C9X13.4",
    "C8X18.75",
    "C9X15",
    "C8X13.75",
    "C8X11.5",
    "C7X14.75",
    "C7X12.25",
    "C7X9.8",
    "C6X10.5",
    "C6X13",
    "C6X8.2",
    "C5X9",
    "C4X7.25",
    "C4X5.4",
    "C4X6.25",
    "C3X6",
    "C4X4.5",
    "C3X5",
    "C3X4.1",
    "C3X3.5",
    "C5X6.7",
    "MC18X51.9",
    "MC18X58",
    "MC18X42.7",
    "MC18X45.8",
    "MC13X50",
    "MC13X40",
    "MC13X35",
    "MC12X50",
    "MC13X31.8",
    "MC12X45",
    "MC12X40",
    "MC12X35",
    "MC12X14.3",
    "MC12X10.6",
    "MC12X31",
    "MC10X33.6",
    "MC10X41.1",
    "MC10X22",
    "MC10X28.5",
    "MC10X6.5",
    "MC10X25",
    "MC10X8.4",
    "MC9X25.4",
    "MC8X21.4",
    "MC9X23.9",
    "MC8X22.8",
    "MC8X8.5",
    "MC7X22.7",
    "MC7X19.1",
    "MC8X18.7",
    "MC8X20",
    "MC6X18",
    "MC6X15.1",
    "MC6X16.3",
    "MC6X12",
    "MC6X15.3",
    "MC6X7",
    "MC4X13.8",
    "MC6X6.5",
    "MC3X7.1",
)
