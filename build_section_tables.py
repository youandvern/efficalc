"""
This script can be used to build the sections database that is packaged with the library. It reads the individual CSV
files for each section type and writes them to a table in the sections database with an index on the AISC_name column.
"""

import sqlite3

# pandas is not required for any functionality in the efficalc package, so it is excluded from the requirements. It is
# only used to build the sections database that is packaged with the library.
import pandas as pd

from efficalc.sections.section_query import (
    AISC_ANGLE_TABLE,
    AISC_CHANNEL_TABLE,
    AISC_CIRCULAR_TABLE,
    AISC_DOUBLE_ANGLE_TABLE,
    AISC_RECTANGULAR_TABLE,
    AISC_TEE_TABLE,
    AISC_WIDE_FLANGE_TABLE,
    SECTIONS_DB_NAME,
)

if __name__ == "__main__":
    conn = sqlite3.connect(f"efficalc/sections/{SECTIONS_DB_NAME}")

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_2L.csv")
    df.to_sql(AISC_DOUBLE_ANGLE_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_DOUBLE_ANGLE_TABLE} ON {AISC_DOUBLE_ANGLE_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_channel.csv")
    df.to_sql(AISC_CHANNEL_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_CHANNEL_TABLE} ON {AISC_CHANNEL_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_circular.csv")
    df.to_sql(AISC_CIRCULAR_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_CIRCULAR_TABLE} ON {AISC_CIRCULAR_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_L.csv")
    df.to_sql(AISC_ANGLE_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_ANGLE_TABLE} ON {AISC_ANGLE_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_rectangular.csv")
    df.to_sql(AISC_RECTANGULAR_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_RECTANGULAR_TABLE} ON {AISC_RECTANGULAR_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_T.csv")
    df.to_sql(AISC_TEE_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_TEE_TABLE} ON {AISC_TEE_TABLE}(AISC_name);"
    )

    df = pd.read_csv("efficalc/sections/csv/aisc_sections_WF.csv")
    df.to_sql(AISC_WIDE_FLANGE_TABLE, conn, if_exists="replace", index=False)
    conn.execute(
        f"CREATE UNIQUE INDEX unique_aisc_name_{AISC_WIDE_FLANGE_TABLE} ON {AISC_WIDE_FLANGE_TABLE}(AISC_name);"
    )

    conn.close()
