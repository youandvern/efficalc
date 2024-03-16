import dataclasses


@dataclasses.dataclass
class AiscCircular(object):
    """This is a dataclass containing the properties of an AISC Circular section. Properties follow the AISC shapes
    database.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param AISC_name: The name of the AISC section
    :type AISC_name: str
    :param C: HSS torsional constant (in^3)
    :type C: float
    :param D_t: Slenderness ratio for round HSS and pipe, D/t
    :type D_t: float
    :param EDI_Std_Nomenclature: The EDI standard nomenclature name
    :type EDI_Std_Nomenclature: str
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param J: Torsional constant (in^4)
    :type J: float
    :param OD: Outside diameter of round HSS or pipe (in)
    :type OD: float
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
    :param Zx: Plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^3)
    :type Zy: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param tdes: Design thickness of HSS and pipe wall (in)
    :type tdes: float
    :param tnom: Nominal thickness of HSS and pipe wall (in)
    :type tnom: float
    """

    A: float
    AISC_name: str
    C: float
    D_t: float
    EDI_Std_Nomenclature: str
    Ix: float
    Iy: float
    J: float
    OD: float
    Sx: float
    Sy: float
    T_F: str
    Type: str
    W: float
    Zx: float
    Zy: float
    rx: float
    ry: float
    tdes: float
    tnom: float


ALL_AISC_CIRCULAR_NAMES = (
    "HSS20.000X0.500",
    "HSS20.000X0.375",
    "HSS18.000X0.500",
    "HSS18.000X0.375",
    "HSS16.000X0.312",
    "HSS16.000X0.375",
    "HSS16.000X0.625",
    "HSS16.000X0.500",
    "HSS14.000X0.312",
    "HSS10.750X0.250",
    "HSS10.000X0.625",
    "HSS10.000X0.500",
    "HSS10.000X0.375",
    "HSS10.000X0.312",
    "HSS10.000X0.250",
    "HSS10.000X0.188",
    "HSS9.625X0.500",
    "HSS9.625X0.375",
    "HSS9.625X0.312",
    "HSS9.625X0.250",
    "HSS9.625X0.188",
    "HSS8.625X0.625",
    "HSS8.625X0.500",
    "HSS16.000X0.438",
    "HSS8.625X0.375",
    "HSS8.625X0.322",
    "HSS16.000X0.250",
    "HSS14.000X0.625",
    "HSS14.000X0.500",
    "HSS14.000X0.375",
    "HSS10.750X0.500",
    "HSS12.750X0.375",
    "HSS12.750X0.250",
    "HSS14.000X0.250",
    "HSS8.625X0.188",
    "HSS12.750X0.500",
    "HSS10.750X0.375",
    "HSS8.625X0.250",
    "HSS7.500X0.500",
    "HSS7.500X0.312",
    "HSS7.625X0.375",
    "HSS7.500X0.375",
    "HSS7.625X0.328",
    "HSS7.500X0.250",
    "HSS7.500X0.188",
    "HSS7.000X0.375",
    "HSS7.000X0.500",
    "HSS7.000X0.312",
    "HSS7.000X0.250",
    "HSS7.000X0.188",
    "HSS7.000X0.125",
    "HSS6.875X0.500",
    "HSS6.875X0.375",
    "HSS6.875X0.250",
    "HSS6.875X0.188",
    "HSS6.625X0.500",
    "HSS6.625X0.432",
    "HSS6.625X0.375",
    "HSS6.625X0.312",
    "HSS6.625X0.280",
    "HSS6.625X0.188",
    "HSS6.625X0.250",
    "HSS6.625X0.125",
    "HSS6.000X0.500",
    "HSS6.000X0.375",
    "HSS6.000X0.312",
    "HSS6.000X0.280",
    "HSS6.000X0.250",
    "HSS6.000X0.188",
    "HSS6.000X0.125",
    "HSS6.875X0.312",
    "HSS5.563X0.500",
    "HSS5.563X0.375",
    "HSS5.563X0.258",
    "HSS5.563X0.188",
    "HSS5.563X0.134",
    "HSS5.500X0.500",
    "HSS5.500X0.375",
    "HSS5.500X0.258",
    "HSS5.000X0.500",
    "HSS5.000X0.375",
    "HSS5.000X0.312",
    "HSS5.000X0.250",
    "HSS5.000X0.258",
    "HSS5.000X0.188",
    "HSS5.000X0.125",
    "HSS4.500X0.375",
    "HSS4.500X0.337",
    "HSS4.500X0.237",
    "HSS4.500X0.188",
    "HSS4.500X0.125",
    "HSS4.000X0.313",
    "HSS4.000X0.250",
    "HSS4.000X0.237",
    "HSS4.000X0.226",
    "HSS4.000X0.220",
    "HSS4.000X0.188",
    "HSS3.500X0.313",
    "HSS4.000X0.125",
    "HSS3.500X0.300",
    "HSS3.500X0.250",
    "HSS3.500X0.216",
    "HSS3.500X0.203",
    "HSS3.500X0.188",
    "HSS3.000X0.250",
    "HSS3.000X0.216",
    "HSS3.500X0.125",
    "HSS3.000X0.203",
    "HSS3.000X0.188",
    "HSS3.000X0.152",
    "HSS3.000X0.134",
    "HSS3.000X0.125",
    "HSS2.875X0.203",
    "HSS2.875X0.250",
    "HSS2.500X0.188",
    "HSS2.875X0.188",
    "HSS2.875X0.125",
    "HSS2.375X0.218",
    "HSS2.500X0.250",
    "HSS2.375X0.250",
    "HSS2.500X0.125",
    "HSS2.375X0.188",
    "HSS2.375X0.125",
    "HSS2.375X0.154",
    "HSS1.660X0.140",
    "HSS1.900X0.120",
    "Pipe24STD",
    "HSS1.900X0.188",
    "Pipe26STD",
    "Pipe18STD",
    "Pipe14STD",
    "Pipe20STD",
    "Pipe12STD",
    "Pipe10STD",
    "Pipe8STD",
    "Pipe6STD",
    "Pipe4STD",
    "Pipe3-1/2STD",
    "Pipe3STD",
    "Pipe16STD",
    "Pipe5STD",
    "HSS1.900X0.145",
    "Pipe2-1/2STD",
    "Pipe2STD",
    "Pipe26XS",
    "Pipe10XS",
    "Pipe8XS",
    "Pipe6XS",
    "Pipe5XS",
    "Pipe4XS",
    "Pipe3-1/2XS",
    "Pipe3XS",
    "Pipe2-1/2XS",
    "Pipe1STD",
    "Pipe2XS",
    "Pipe1-1/2XS",
    "Pipe1-1/4XS",
    "Pipe1-1/2STD",
    "Pipe3/4XS",
    "Pipe1XS",
    "Pipe12XXS",
    "Pipe10XXS",
    "Pipe1/2XS",
    "Pipe8XXS",
    "Pipe1-1/4STD",
    "Pipe18XS",
    "Pipe3/4STD",
    "Pipe16XS",
    "Pipe20XS",
    "Pipe1/2STD",
    "Pipe14XS",
    "Pipe12XS",
    "Pipe6XXS",
    "Pipe4XXS",
    "Pipe5XXS",
    "Pipe3XXS",
    "Pipe2-1/2XXS",
    "Pipe2XXS",
    "Pipe24XS",
)
