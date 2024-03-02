import dataclasses


@dataclasses.dataclass
class Angle(object):
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
