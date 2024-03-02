import dataclasses


@dataclasses.dataclass
class Channel(object):
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
    twdetl2: float
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
