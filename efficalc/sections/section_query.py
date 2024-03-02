import os
import sqlite3

from efficalc.sections.aisc_angle import Angle
from efficalc.sections.aisc_channel import Channel
from efficalc.sections.aisc_circular import Circular
from efficalc.sections.aisc_double_angle import DoubleAngle
from efficalc.sections.aisc_rectangular import Rectangular
from efficalc.sections.aisc_tee import Tee
from efficalc.sections.aisc_wide_flange import WideFlange

SECTIONS_DB_NAME = "section_properties.db"

AISC_ANGLE_TABLE = "aisc_angle"
AISC_CHANNEL_TABLE = "aisc_channel"
AISC_CIRCULAR_TABLE = "aisc_circular"
AISC_DOUBLE_ANGLE_TABLE = "aisc_double_angle"
AISC_RECTANGULAR_TABLE = "aisc_rectangular"
AISC_TEE_TABLE = "aisc_tee"
AISC_WIDE_FLANGE_TABLE = "aisc_wide_flange"

SECTION_SIZE_NAME_COLUMN = "AISC_name"


def get_aisc_angle(section_size: str) -> Angle:
    row = _fetch_section_row(AISC_ANGLE_TABLE, section_size)

    if row:
        return Angle(**row)
    else:
        raise ValueError(
            f"The AISC angle section size named {section_size} could not be found."
        )


def get_aisc_channel(section_size: str) -> Channel:
    row = _fetch_section_row(AISC_CHANNEL_TABLE, section_size)

    if row:
        return Channel(**row)
    else:
        raise ValueError(
            f"The AISC channel section size named {section_size} could not be found."
        )


def get_aisc_circular(section_size: str) -> Circular:
    row = _fetch_section_row(AISC_CIRCULAR_TABLE, section_size)

    if row:
        return Circular(**row)
    else:
        raise ValueError(
            f"The AISC circular section size named {section_size} could not be found."
        )


def get_aisc_double_angle(section_size: str) -> DoubleAngle:
    row = _fetch_section_row(AISC_DOUBLE_ANGLE_TABLE, section_size)

    if row:
        return DoubleAngle(**row)
    else:
        raise ValueError(
            f"The AISC double angle section size named {section_size} could not be found."
        )


def get_aisc_rectangular(section_size: str) -> Rectangular:
    row = _fetch_section_row(AISC_RECTANGULAR_TABLE, section_size)

    if row:
        return Rectangular(**row)
    else:
        raise ValueError(
            f"The AISC rectangular section size named {section_size} could not be found."
        )


def get_aisc_tee(section_size: str) -> Tee:
    row = _fetch_section_row(AISC_TEE_TABLE, section_size)

    if row:
        return Tee(**row)
    else:
        raise ValueError(
            f"The AISC tee section size named {section_size} could not be found."
        )


def get_aisc_wide_flange(section_size: str) -> WideFlange:
    row = _fetch_section_row(AISC_WIDE_FLANGE_TABLE, section_size)

    if row:
        return WideFlange(**row)
    else:
        raise ValueError(
            f"The AISC wide flange section size named {section_size} could not be found."
        )


def _fetch_section_row(table: str, section_size: str):
    database_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(database_dir, SECTIONS_DB_NAME)
    conn = sqlite3.connect(db_path)

    # Format returned rows as a dictionary-like object with key accessors
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE {SECTION_SIZE_NAME_COLUMN} = ?;",
        (section_size,),
    )
    row = cursor.fetchone()
    conn.close()
    return row
