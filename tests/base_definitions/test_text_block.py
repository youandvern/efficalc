import pytest

from efficalc import (
    TextBlock,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
)


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


def test_save_calc_item(common_setup_teardown):
    h = TextBlock("This is a test", reference="a ref")
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert isinstance(saved_items[0], TextBlock) is True
    assert saved_items[0] == h
    assert saved_items[0].reference == "a ref"


def test_public_members(common_setup_teardown):
    h = TextBlock("This is a test", reference="that's ref")
    assert h.text == "This is a test"
    assert h.description == h.text
    assert h.reference == "that's ref"


def test_to_str(common_setup_teardown):
    h = TextBlock("This is a test")
    assert str(h) == "This is a test"
