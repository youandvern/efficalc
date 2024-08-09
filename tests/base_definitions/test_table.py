import pytest

from efficalc import (
    InputTable,
    Table,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
    set_input_default_overrides,
)


@pytest.fixture
def common_setup_teardown():
    yield 5  # Provide data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


def test_default_values(common_setup_teardown):
    a = Table([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert a.data == [[1, 2, 3, 4], [5, 6, 7, 8]]
    assert a.headers is None
    assert a.title is None
    assert a.striped is False
    assert a.full_width is False
    assert a.result_check is False


def test_set_values(common_setup_teardown):
    a = Table(
        [[1, 2, 3, 4], [5, 6, 7, 8]],
        headers=["a", "b", "c", "d"],
        title="my table",
        striped=True,
        full_width=False,
        result_check=True,
    )
    assert a.data == [[1, 2, 3, 4], [5, 6, 7, 8]]
    assert a.headers == ["a", "b", "c", "d"]
    assert a.title == "my table"
    assert a.striped is True
    assert a.full_width is False
    assert a.result_check is True


def test_save_calc_item(common_setup_teardown):
    b = Table([[1, 2, 3, 4], [5, 6, 7, 8]], headers=["a", "b"])
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b


def test_input_table_save_calc_item(common_setup_teardown):
    b = InputTable([[1, 2, 3, 4], [5, 6, 7, 8]], headers=["a", "b"])
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == b


def test_input_table_set_values(common_setup_teardown):
    a = InputTable(
        [[1, 2, 3, 4], [5, 6, 7, "test"]],
        headers=["a", "b", "c", "d"],
        title="my table",
        striped=True,
        full_width=False,
    )
    assert a.data == [[1, 2, 3, 4], [5, 6, 7, "test"]]
    assert a.headers == ["a", "b", "c", "d"]
    assert a.title == "my table"
    assert a.striped is True
    assert a.full_width is False
    assert a.result_check is False


def test_input_table_identifier(common_setup_teardown):
    a = InputTable([[1, 2, 3, 4], [5, 6, 7, "test"]], headers=["a", "b b"])
    assert a.identifier == "input_table-a-b b"


def test_input_table_with_override_value(common_setup_teardown):
    set_input_default_overrides({"input_table-a-b": [[9, 9, "test"]]})
    a = InputTable([[1, 2, 3, 4], [5, 6, 7, 8]], headers=["a", "b"])
    assert a.data == [[9, 9, "test"]]
    assert a.headers == ["a", "b"]
    assert a.title is None
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == a


def test_input_table_with_empty_override_value(common_setup_teardown):
    set_input_default_overrides({"input_table-a-b": []})
    a = InputTable([[1, 2, 3, 4], [5, 6, 7, 8]], headers=["a", "b"])
    assert a.data == []
    assert a.headers == ["a", "b"]
    assert a.title is None
    saved_items = get_all_calc_objects()
    assert len(saved_items) == 1
    assert saved_items[0] == a
