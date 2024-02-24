import pytest

from efficalc import (
    Heading,
    clear_all_input_default_overrides,
    get_all_calc_objects,
    reset_results,
)


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    reset_results()


def test_save_calc_item(common_setup_teardown):
    h = Heading("This is a test", head_level=5)
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == h
    assert saved_items[0].head_level == 5


def test_public_members(common_setup_teardown):
    h = Heading("This is a test", head_level=5, numbered=False)
    assert h.text == "This is a test"
    assert h.description == h.text
    assert h.head_level == 5
    assert h.numbered is False


def test_to_str(common_setup_teardown):
    h = Heading("This is a test", head_level=5)
    assert str(h) == "This is a test"
