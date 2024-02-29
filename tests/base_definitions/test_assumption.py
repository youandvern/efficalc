import pytest

from efficalc import Assumption, clear_saved_objects, get_all_calc_objects


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


def test_text(common_setup_teardown):
    a = Assumption("This is a test.")
    assert a.text == "This is a test."
    assert str(a) == "This is a test."


def test_save_calc_item(common_setup_teardown):
    b = Assumption("another test")
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b
    assert saved_items[0].text == "another test"
