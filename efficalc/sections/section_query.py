import os
import sqlite3

from efficalc.sections.aisc_angle import AiscAngle
from efficalc.sections.aisc_channel import AiscChannel
from efficalc.sections.aisc_circular import AiscCircular
from efficalc.sections.aisc_double_angle import AiscDoubleAngle
from efficalc.sections.aisc_rectangular import AiscRectangular
from efficalc.sections.aisc_tee import AiscTee
from efficalc.sections.aisc_wide_flange import AiscWideFlange
from efficalc.sections.alum_angle import AluminumAngle
from efficalc.sections.alum_channel import AluminumChannel
from efficalc.sections.alum_circular import AluminumCircular
from efficalc.sections.alum_rectangular import AluminumRectangular
from efficalc.sections.alum_wide_flange import AluminumWideFlange

SECTIONS_DB_NAME = "section_properties.db"

AISC_ANGLE_TABLE = "aisc_angle"
AISC_CHANNEL_TABLE = "aisc_channel"
AISC_CIRCULAR_TABLE = "aisc_circular"
AISC_DOUBLE_ANGLE_TABLE = "aisc_double_angle"
AISC_RECTANGULAR_TABLE = "aisc_rectangular"
AISC_TEE_TABLE = "aisc_tee"
AISC_WIDE_FLANGE_TABLE = "aisc_wide_flange"
ALUM_ANGLE_TABLE = "aluminum_angle"
ALUM_CHANNEL_TABLE = "aluminum_channel"
ALUM_CIRCULAR_TABLE = "aluminum_circular"
ALUM_RECTANGULAR_TABLE = "aluminum_rectangular"
ALUM_WIDE_FLANGE_TABLE = "aluminum_wide_flange"

AISC_SECTION_SIZE_NAME_COLUMN = "AISC_name"
ALUM_SECTION_SIZE_NAME_COLUMN = "Size"


def get_aisc_angle(section_size: str) -> AiscAngle:
    """Fetches the properties of a specified AISC Angle section from the sections database and returns an
    :class:`efficalc.sections.AiscAngle` instance populated with these properties.

    :param section_size: The designation of the angle section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: An Angle populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscAngle`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """
    row = _fetch_aisc_section_row(AISC_ANGLE_TABLE, section_size)

    if row:
        return AiscAngle(**row)
    else:
        raise ValueError(
            f"The AISC angle section size named {section_size} could not be found."
        )


def get_aisc_channel(section_size: str) -> AiscChannel:
    """
    Fetches the properties of a specified AISC Channel section from the sections database and returns a
    :class:`efficalc.sections.AiscChannel` instance populated with these properties.

    :param section_size: The designation of the channel section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A Channel populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscChannel`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_CHANNEL_TABLE, section_size)

    if row:
        return AiscChannel(**row)
    else:
        raise ValueError(
            f"The AISC channel section size named {section_size} could not be found."
        )


def get_aisc_circular(section_size: str) -> AiscCircular:
    """
    Fetches the properties of a specified AISC Circular section from the sections database and returns a
    :class:`efficalc.sections.AiscCircular` instance populated with these properties.

    :param section_size: The designation of the circular section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A Circular populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscCircular`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_CIRCULAR_TABLE, section_size)

    if row:
        return AiscCircular(**row)
    else:
        raise ValueError(
            f"The AISC circular section size named {section_size} could not be found."
        )


def get_aisc_double_angle(section_size: str) -> AiscDoubleAngle:
    """
    Fetches the properties of a specified AISC Double Angle section from the sections database and returns a
    :class:`efficalc.sections.AiscDoubleAngle` instance populated with these properties.

    :param section_size: The designation of the double angle section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A DoubleAngle populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscDoubleAngle`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_DOUBLE_ANGLE_TABLE, section_size)

    if row:
        return AiscDoubleAngle(**row)
    else:
        raise ValueError(
            f"The AISC double angle section size named {section_size} could not be found."
        )


def get_aisc_rectangular(section_size: str) -> AiscRectangular:
    """
    Fetches the properties of a specified AISC Rectangular section from the sections database and returns a
    :class:`efficalc.sections.AiscRectangular` instance populated with these properties.

    :param section_size: The designation of the rectangular section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A Rectangular populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscRectangular`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_RECTANGULAR_TABLE, section_size)

    if row:
        return AiscRectangular(**row)
    else:
        raise ValueError(
            f"The AISC rectangular section size named {section_size} could not be found."
        )


def get_aisc_tee(section_size: str) -> AiscTee:
    """
    Fetches the properties of a specified AISC Tee section from the sections database and returns a
    :class:`efficalc.sections.AiscTee` instance populated with these properties.

    :param section_size: The designation of the tee section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A Tee populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscTee`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_TEE_TABLE, section_size)

    if row:
        return AiscTee(**row)
    else:
        raise ValueError(
            f"The AISC tee section size named {section_size} could not be found."
        )


def get_aisc_wide_flange(section_size: str) -> AiscWideFlange:
    """
    Fetches the properties of a specified AISC Wide Flange section from the sections database and returns a
    :class:`efficalc.sections.AiscWideFlange` instance populated with these properties.

    :param section_size: The designation of the wide flange section size as the AISC_name property defined in the database.
    :type section_size: str
    :return: A WideFlange populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AiscWideFlange`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aisc_section_row(AISC_WIDE_FLANGE_TABLE, section_size)

    if row:
        return AiscWideFlange(**row)
    else:
        raise ValueError(
            f"The AISC wide flange section size named {section_size} could not be found."
        )


def get_aluminum_angle(section_size: str) -> AluminumAngle:
    """
    Fetches the properties of a specified Aluminum Angle section from the sections database and returns a
    :class:`efficalc.sections.AluminumAngle` instance populated with these properties.

    :param section_size: The designation of the aluminum section size as the Size property defined in the database.
    :type section_size: str
    :return: An AluminumAngle populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AluminumAngle`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aluminum_section_row(ALUM_ANGLE_TABLE, section_size)

    if row:
        return AluminumAngle(**row)
    else:
        raise ValueError(
            f"The aluminum angle section size named {section_size} could not be found."
        )


def get_aluminum_channel(section_size: str) -> AluminumChannel:
    """
    Fetches the properties of a specified Aluminum Channel section from the sections database and returns a
    :class:`efficalc.sections.AluminumChannel` instance populated with these properties.

    :param section_size: The designation of the aluminum section size as the Size property defined in the database.
    :type section_size: str
    :return: An AluminumChannel populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AluminumChannel`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aluminum_section_row(ALUM_CHANNEL_TABLE, section_size)

    if row:
        return AluminumChannel(**row)
    else:
        raise ValueError(
            f"The aluminum channel section size named {section_size} could not be found."
        )


def get_aluminum_circular(section_size: str) -> AluminumCircular:
    """
    Fetches the properties of a specified Aluminum Circular section from the sections database and returns a
    :class:`efficalc.sections.AluminumCircular` instance populated with these properties.

    :param section_size: The designation of the aluminum section size as the Size property defined in the database.
    :type section_size: str
    :return: An AluminumCircular populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AluminumCircular`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aluminum_section_row(ALUM_CIRCULAR_TABLE, section_size)

    if row:
        return AluminumCircular(**row)
    else:
        raise ValueError(
            f"The aluminum circular section size named {section_size} could not be found."
        )


def get_aluminum_rectangular(section_size: str) -> AluminumRectangular:
    """
    Fetches the properties of a specified Aluminum Rectangular section from the sections database and returns a
    :class:`efficalc.sections.AluminumRectangular` instance populated with these properties.

    :param section_size: The designation of the aluminum section size as the Size property defined in the database.
    :type section_size: str
    :return: An AluminumRectangular populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AluminumRectangular`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aluminum_section_row(ALUM_RECTANGULAR_TABLE, section_size)

    if row:
        return AluminumRectangular(**row)
    else:
        raise ValueError(
            f"The aluminum rectangular section size named {section_size} could not be found."
        )


def get_aluminum_wide_flange(section_size: str) -> AluminumWideFlange:
    """
    Fetches the properties of a specified Aluminum Wide Flange section from the sections database and returns a
    :class:`efficalc.sections.AluminumWideFlange` instance populated with these properties.

    :param section_size: The designation of the aluminum section size as the Size property defined in the database.
    :type section_size: str
    :return: An AluminumWideFlange populated with the properties of the specified section size.
    :rtype: `efficalc.sections.AluminumWideFlange`
    :raises ValueError: If the specified section size cannot be found in the sections database.
    """

    row = _fetch_aluminum_section_row(ALUM_WIDE_FLANGE_TABLE, section_size)

    if row:
        return AluminumWideFlange(**row)
    else:
        raise ValueError(
            f"The aluminum wide flange section size named {section_size} could not be found."
        )


def _fetch_aisc_section_row(table: str, section_size: str):
    return _fetch_section_row(table, section_size, AISC_SECTION_SIZE_NAME_COLUMN)


def _fetch_aluminum_section_row(table: str, section_size: str):
    return _fetch_section_row(table, section_size, ALUM_SECTION_SIZE_NAME_COLUMN)


def _fetch_section_row(table: str, section_size: str, size_field_name: str):
    database_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(database_dir, SECTIONS_DB_NAME)
    conn = sqlite3.connect(db_path)

    # Format returned rows as a dictionary-like object with key accessors
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE {size_field_name} = ?;",
        (section_size,),
    )
    row = cursor.fetchone()
    conn.close()
    return row
