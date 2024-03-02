import pytest

from efficalc.sections.section_query import (
    get_aisc_angle,
    get_aisc_channel,
    get_aisc_circular,
    get_aisc_double_angle,
    get_aisc_rectangular,
    get_aisc_tee,
    get_aisc_wide_flange,
)


def test_angle_lookup():
    section = get_aisc_angle("L6X4X9/16")
    assert section.d == 4
    assert section.A == 5.31
    assert section.Type == "L"


def test_angle_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_angle("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_channel_lookup():
    section = get_aisc_channel("C12X25")
    assert section.d == 12
    assert section.A == 7.34
    assert section.Type == "C"


def test_channel_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_channel("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_circular_lookup():
    section = get_aisc_circular("HSS18.000X0.375")
    assert section.W == 70.66
    assert section.A == 19.4
    assert section.Type == "HSS"


def test_circular_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_circular("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_double_angle_lookup():
    section = get_aisc_double_angle("2L12X12X1-1/8")
    assert section.W == 174
    assert section.A == 51.6
    assert section.Type == "2L"


def test_double_angle_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_double_angle("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_rectangular_lookup():
    section = get_aisc_rectangular("HSS20X8X5/8")
    assert section.W == 110.36
    assert section.A == 30.3
    assert section.Type == "HSS"


def test_rectangular_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_rectangular("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_tee_lookup():
    section = get_aisc_tee("WT20X198.5")
    assert section.W == 198.5
    assert section.A == 58.3
    assert section.Type == "WT"


def test_tee_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_tee("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_wide_flange_lookup():
    section = get_aisc_wide_flange("W14X109")
    assert section.d == 14.3
    assert section.A == 32
    assert section.Type == "W"


def test_wide_flange_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aisc_wide_flange("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)
