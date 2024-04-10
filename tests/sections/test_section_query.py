import pytest

from efficalc.sections.section_query import (
    get_aisc_angle,
    get_aisc_channel,
    get_aisc_circular,
    get_aisc_double_angle,
    get_aisc_rectangular,
    get_aisc_tee,
    get_aisc_wide_flange,
    get_aluminum_angle,
    get_aluminum_channel,
    get_aluminum_circular,
    get_aluminum_rectangular,
    get_aluminum_wide_flange,
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


def test_aluminum_angle_lookup():
    section = get_aluminum_angle("L 3 x 2 x 3/8")
    assert section.d == 3
    assert section.b == 2
    assert section.t == 0.375
    assert section.A == 1.74
    assert section.W == 2.05


def test_aluminum_angle_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aluminum_angle("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_aluminum_channel_lookup():
    section = get_aluminum_channel("C 4 X 2.50")
    assert section.d == 4
    assert section.W == 2.50
    assert section.A == 2.13
    assert section.b == 1.72


def test_aluminum_channel_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aluminum_channel("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_aluminum_circular_lookup():
    section = get_aluminum_circular("HSS 6 x 0.25")
    assert section.OD == 6
    assert section.t == 0.25
    assert section.ID == 5.5
    assert section.W == 5.31
    assert section.A == 4.52


def test_aluminum_circular_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aluminum_circular("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_aluminum_rectangular_lookup():
    section = get_aluminum_rectangular("RT 6 x 2 x 1/4")
    assert section.d == 6
    assert section.b == 2
    assert section.t == 0.25
    assert section.W == 4.41
    assert section.A == 3.75


def test_aluminum_rectangular_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aluminum_rectangular("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)


def test_aluminum_wide_flange_lookup():
    section = get_aluminum_wide_flange("WF 6 x 8.30")
    assert section.d == 6
    assert section.W == 8.30
    assert section.b == 6
    assert section.A == 7.06


def test_aluminum_wide_flange_lookup_size_not_found():
    with pytest.raises(ValueError) as e_info:
        get_aluminum_wide_flange("NOT_FOUND")
    assert "section size named NOT_FOUND could not be found" in str(e_info.value)
