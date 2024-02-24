import pytest

from efficalc import (
    Title,
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
    t = Title("This is a test")
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert isinstance(saved_items[0], Title) is True
    assert saved_items[0] == t
    assert saved_items[0].text == "This is a test"


def test_public_members(common_setup_teardown):
    t = Title("This is a test")
    assert t.text == "This is a test"


def test_to_str(common_setup_teardown):
    h = Title("This is a test")
    assert str(h) == "This is a test"
