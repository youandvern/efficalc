import dataclasses


@dataclasses.dataclass
class AiscTee(object):
    """This is a dataclass containing the properties of an AISC Tee section, typically derived from W-shapes,
    M-shapes, or S-shapes by cutting along the web. Properties follow the AISC shapes database.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param AISC_name: The name of the AISC section
    :type AISC_name: str
    :param Cw: Warping constant (in^6)
    :type Cw: float
    :param D_t: Slenderness ratio for tee shapes, D/t where D=d
    :type D_t: float
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
    :param PA: Shape perimeter minus one flange surface, as used in Design Guide 19 (in)
    :type PA: float
    :param PB: Shape perimeter, as used in AISC Design Guide 19 (in)
    :type PB: float
    :param PC: Box perimeter minus one flange surface, as used in Design Guide 19 (in)
    :type PC: float
    :param PD: Box perimeter, as used in AISC Design Guide 19 (in)
    :type PD: float
    :param Sx: Elastic section modulus about the x-axis (in^3)
    :type Sx: float
    :param Sy: Elastic section modulus about the y-axis (in^3)
    :type Sy: float
    :param T_F: Whether the section has an additional note in the AISC shapes database (T or F)
    :type T_F: str
    :param Type: The section type
    :type Type: str
    :param W: Nominal weight (lb/ft)
    :type W: float
    :param WGi: The workable gage for the inner fastener holes in the flange (in)
    :type WGi: float
    :param Zx: Plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^3)
    :type Zy: float
    :param bf: Width of flange (in)
    :type bf: float
    :param bfdet: Detailing value of flange width (in)
    :type bfdet: float
    :param bf_2tf: Slenderness ratio, bf/2tf
    :type bf_2tf: float
    :param d: Overall depth of member (in)
    :type d: float
    :param ddet: Detailing value of member depth (in)
    :type ddet: float
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
    :param tf: Thickness of flange (in)
    :type tf: float
    :param tfdet: Detailing value of flange thickness (in)
    :type tfdet: float
    :param tw: Thickness of web (in)
    :type tw: float
    :param twdet: Detailing value of web thickness (in)
    :type twdet: float
    :param twdet_2: Half the web thickness for detailing purposes, twdet/2  (in)
    :type twdet_2: float
    :param y: Vertical distance from designated edge of member to center of gravity of member (in)
    :type y: float
    :param yp: Vertical distance from designated edge of member to plastic neutral axis of member (in)
    :type yp: float
    """

    A: float
    AISC_name: str
    Cw: float
    D_t: float
    EDI_Std_Nomenclature: str
    H: float
    Ix: float
    Iy: float
    J: float
    PA: float
    PB: float
    PC: float
    PD: float
    Sx: float
    Sy: float
    T_F: str
    Type: str
    W: float
    WGi: float
    Zx: float
    Zy: float
    bf: float
    bfdet: float
    bf_2tf: float
    d: float
    ddet: float
    kdes: float
    kdet: float
    ro: float
    rx: float
    ry: float
    tf: float
    tfdet: float
    tw: float
    twdet: float
    twdet_2: float
    y: float
    yp: float


ALL_AISC_TEE_NAMES = (
    "WT22X167.5",
    "WT20X327.5",
    "WT22X115",
    "WT22X145",
    "WT20X198.5",
    "WT20X296.5",
    "WT20X251.5",
    "WT22X131",
    "WT20X215.5",
    "WT20X148.5",
    "WT20X186",
    "WT20X181",
    "WT20X162",
    "WT20X163.5",
    "WT20X196",
    "WT20X99.5",
    "WT20X165.5",
    "WT20X124.5",
    "WT20X107.5",
    "WT20X138.5",
    "WT20X105.5",
    "WT20X83.5",
    "WT20X91.5",
    "WT20X147",
    "WT20X139",
    "WT20X117.5",
    "WT20X132",
    "WT18X326",
    "WT18X401",
    "WT18X361.5",
    "WT20X74.5",
    "WT18X462.5",
    "WT18X220.5",
    "WT18X426.5",
    "WT18X264.5",
    "WT18X165",
    "WT18X243.5",
    "WT18X197.5",
    "WT18X180.5",
    "WT18X151",
    "WT18X131",
    "WT18X141",
    "WT18X123.5",
    "WT18X116",
    "WT18X105",
    "WT18X128",
    "WT18X91",
    "WT18X85",
    "WT18X97",
    "WT18X80",
    "WT18X75",
    "WT18X67.5",
    "WT16.5X193.5",
    "WT16.5X177",
    "WT16.5X159",
    "WT16.5X145.5",
    "WT16.5X131.5",
    "WT18X115.5",
    "WT16.5X120.5",
    "WT16.5X110.5",
    "WT16.5X100.5",
    "WT16.5X84.5",
    "WT16.5X76",
    "WT16.5X65",
    "WT16.5X70.5",
    "WT15X178.5",
    "WT16.5X59",
    "WT15X195.5",
    "WT15X117.5",
    "WT15X163",
    "WT15X146",
    "WT13.5X269.5",
    "WT15X130.5",
    "WT15X86.5",
    "WT13.5X184",
    "WT13.5X168",
    "WT13.5X153.5",
    "WT15X54",
    "WT15X62",
    "WT15X58",
    "WT15X95.5",
    "WT15X66",
    "WT13.5X140.5",
    "WT15X74",
    "WT15X49.5",
    "WT13.5X117.5",
    "WT15X45",
    "WT13.5X108.5",
    "WT15X105.5",
    "WT13.5X129",
    "WT13.5X80.5",
    "WT13.5X89",
    "WT13.5X97",
    "WT13.5X64.5",
    "WT13.5X57",
    "WT13.5X73",
    "WT13.5X51",
    "WT13.5X47",
    "WT13.5X42",
    "WT12X167.5",
    "WT12X185",
    "WT12X139.5",
    "WT12X153",
    "WT12X125",
    "WT12X114.5",
    "WT12X103.5",
    "WT12X96",
    "WT12X88",
    "WT12X81",
    "WT12X73",
    "WT12X65.5",
    "WT12X58.5",
    "WT12X51.5",
    "WT12X52",
    "WT12X47",
    "WT12X38",
    "WT12X34",
    "WT12X42",
    "WT12X31",
    "WT10.5X137.5",
    "WT10.5X124",
    "WT12X27.5",
    "WT10.5X111.5",
    "WT10.5X100.5",
    "WT10.5X66",
    "WT10.5X91",
    "WT10.5X24",
    "WT10.5X55.5",
    "WT10.5X28.5",
    "WT10.5X25",
    "WT10.5X50.5",
    "WT9X141.5",
    "WT9X155.5",
    "WT10.5X22",
    "WT9X105.5",
    "WT9X129",
    "WT10.5X46.5",
    "WT9X117",
    "WT10.5X61",
    "WT9X96",
    "WT9X87.5",
    "WT10.5X34",
    "WT10.5X73.5",
    "WT10.5X27.5",
    "WT10.5X41.5",
    "WT9X71.5",
    "WT10.5X31",
    "WT10.5X36.5",
    "WT9X79",
    "WT9X53",
    "WT10.5X83",
    "WT9X43",
    "WT9X59.5",
    "WT9X65",
    "WT9X35.5",
    "WT9X38",
    "WT9X27.5",
    "WT9X32.5",
    "WT9X30",
    "WT9X48.5",
    "WT8X38.5",
    "WT9X20",
    "WT9X25",
    "WT8X33.5",
    "WT8X25",
    "WT8X28.5",
    "WT8X22.5",
    "WT9X17.5",
    "WT8X18",
    "WT8X15.5",
    "WT8X20",
    "WT8X13",
    "WT7X436.5",
    "WT9X23",
    "WT8X50",
    "WT8X44.5",
    "WT7X404",
    "WT7X365",
    "WT7X332.5",
    "WT7X302.5",
    "WT7X275",
    "WT7X250",
    "WT7X227.5",
    "WT7X213",
    "WT7X185",
    "WT7X199",
    "WT7X171",
    "WT7X155.5",
    "WT7X141.5",
    "WT7X128.5",
    "WT7X116.5",
    "WT7X105.5",
    "WT7X96.5",
    "WT7X88",
    "WT7X79.5",
    "WT7X72.5",
    "WT7X66",
    "WT7X60",
    "WT7X49.5",
    "WT7X45",
    "WT7X54.5",
    "WT7X37",
    "WT7X34",
    "WT7X41",
    "WT7X30.5",
    "WT7X26.5",
    "WT7X24",
    "WT7X21.5",
    "WT7X19",
    "WT7X17",
    "WT7X15",
    "WT7X13",
    "WT7X11",
    "WT6X152.5",
    "WT6X139.5",
    "WT6X126",
    "WT6X105",
    "WT6X115",
    "WT6X95",
    "WT6X168",
    "WT6X85",
    "WT6X53",
    "WT6X68",
    "WT6X76",
    "WT6X60",
    "WT6X39.5",
    "WT6X48",
    "WT6X32.5",
    "WT6X43.5",
    "WT6X36",
    "WT6X26.5",
    "WT6X22.5",
    "WT6X29",
    "WT6X25",
    "WT6X20",
    "WT6X17.5",
    "WT6X15",
    "WT6X13",
    "WT6X11",
    "WT6X9.5",
    "WT6X8",
    "WT6X7",
    "WT5X56",
    "WT5X50",
    "WT5X44",
    "WT5X38.5",
    "WT5X30",
    "WT5X34",
    "WT5X27",
    "WT5X24.5",
    "WT5X22.5",
    "WT5X19.5",
    "WT5X16.5",
    "WT5X15",
    "WT5X13",
    "WT5X11",
    "WT5X9.5",
    "WT5X8.5",
    "WT5X7.5",
    "WT5X6",
    "WT4X33.5",
    "WT4X29",
    "WT4X24",
    "WT4X20",
    "WT4X17.5",
    "WT4X15.5",
    "WT4X14",
    "WT4X12",
    "WT4X10.5",
    "WT4X9",
    "WT4X7.5",
    "WT4X6.5",
    "WT4X5",
    "WT3X12.5",
    "WT3X10",
    "WT3X7.5",
    "WT3X8",
    "WT3X6",
    "WT3X4.5",
    "WT3X4.25",
    "WT2.5X9.5",
    "WT2.5X8",
    "WT2X6.5",
    "MT6.25X6.2",
    "MT6.25X5.8",
    "MT6X5.9",
    "MT6X5.4",
    "MT6X5",
    "MT5X4.5",
    "MT5X4",
    "MT5X3.75",
    "MT4X3.25",
    "MT4X3.1",
    "MT3X2.2",
    "MT3X1.85",
    "MT2.5X9.45",
    "MT2X3",
    "ST12X60.5",
    "ST12X53",
    "ST12X50",
    "ST12X40",
    "ST10X48",
    "ST12X45",
    "ST10X43",
    "ST10X37.5",
    "ST9X27.35",
    "ST10X33",
    "ST7.5X25",
    "ST9X35",
    "ST6X20.4",
    "ST6X17.5",
    "ST6X25",
    "ST7.5X21.45",
    "ST6X15.9",
    "ST5X17.5",
    "ST5X12.7",
    "ST4X9.2",
    "ST4X11.5",
    "ST3X8.6",
    "ST3X6.25",
    "ST2.5X5",
    "ST2X4.75",
    "ST2X3.85",
    "ST1.5X3.75",
    "ST1.5X2.85",
)
