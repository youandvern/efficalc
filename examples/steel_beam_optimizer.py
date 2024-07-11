from efficalc import clear_saved_objects

# This is importing the calculation file for https://www.efficalc.com/public-calc/design/steel-beam-calculator
from .steel_beam_moment_strength import calculation as steel_beam_moment_strength


def calculation():
    """This is a simple function that will find the lightest beam size that is strong enough for the input properties."""

    # Loop through all available beam sizes starting at the lightest beam
    for name in EFFICIENT_AISC_WIDE_FLANGE_BEAM_NAMES_BY_WT:

        # Clear calculations from any previous run
        clear_saved_objects()

        # Run the strength calculation for the current beam
        beam_design = steel_beam_moment_strength(name)

        # If the beam is strong enough, finsh the calculation without clearing the saved objects. The last run is the
        # most efficient section. If it's not strong enough, continue the loop to the next heavier section.
        if beam_design.get("design_strength") >= beam_design.get("demand"):
            return


# These are the W-Shapes Selection by Zx (AISC 14th edition Table 3-2) sorted by nominal weight (and depth)
EFFICIENT_AISC_WIDE_FLANGE_BEAM_NAMES_BY_WT = [
    "W8X10",
    "W10X12",
    "W12X14",
    "W12X16",
    "W10X19",
    "W12X19",
    "W10X22",
    "W12X22",
    "W14X22",
    "W12X26",
    "W14X26",
    "W16X26",
    "W14X30",
    "W16X31",
    "W14X34",
    "W18X35",
    "W16X40",
    "W18X40",
    "W21X44",
    "W21X48",
    "W21X50",
    "W18X55",
    "W21X55",
    "W24X55",
    "W21X62",
    "W24X62",
    "W21X68",
    "W24X68",
    "W24X76",
    "W24X84",
    "W27X84",
    "W30X90",
    "W30X99",
    "W30X108",
    "W30X116",
    "W33X118",
    "W33X130",
    "W36X135",
    "W33X141",
    "W40X149",
    "W36X160",
    "W40X167",
]
