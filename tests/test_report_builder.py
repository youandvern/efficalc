import os
from unittest.mock import mock_open, patch

import pytest

from efficalc import Calculation, Input, clear_saved_objects
from efficalc.report_builder import ReportBuilder


@pytest.fixture
def calc_function():
    def calc():
        a = Input("a", 4, "in")
        Calculation("calc", a**2 + a + 2, "in^2")

    yield calc  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


@pytest.fixture
def temp_file_path():
    yield "/fake/temp/file.html"


@pytest.fixture
def mock_create_temp_html_file(temp_file_path):
    """Prevent tests from writing files to disk"""
    with patch(
        "efficalc.report_builder._create_temp_html_file",
        return_value=temp_file_path,
    ) as mock:
        yield mock


@pytest.fixture
def mock_builtin_open():
    """Mock the built-in open method within the report_builder module."""
    mock_file_handler = mock_open()
    with patch("builtins.open", mock_file_handler) as mock:
        yield mock


@pytest.fixture
def mock_webbrowser_open():
    """Prevent tests from opening a web browser"""
    with patch("webbrowser.open") as mock:
        yield mock


@pytest.fixture
def mock_os_path_exists():
    """Prevent tests from checking if a file exists on the current file system"""
    with patch("os.path.exists", return_value=True) as mock:
        yield mock


@pytest.fixture
def mock_os_path_does_not_exist():
    """Prevent tests from checking if a file exists on the current file system"""
    with patch("os.path.exists", return_value=False) as mock:
        yield mock


@pytest.fixture
def mock_os_makedirs():
    """Prevent tests from making a directory on the current file system"""
    with patch("os.makedirs") as mock:
        yield mock


def test_view_report_creates_temp_calc_file_and_opens_in_browser(
    calc_function, mock_webbrowser_open, mock_create_temp_html_file, temp_file_path
):
    report_builder = ReportBuilder(calc_function=calc_function)
    report_path = report_builder.view_report()

    assert report_path == temp_file_path

    mock_create_temp_html_file.assert_called_once()
    mock_webbrowser_open.assert_called_once_with(
        "file://" + os.path.realpath(temp_file_path)
    )

    report_content = mock_create_temp_html_file.call_args[0][0]
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content


def test_get_html_as_str_creates_html_file(calc_function):
    report_builder = ReportBuilder(calc_function=calc_function)
    report_content = report_builder.get_html_as_str()
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content


def test_save_report_writes_to_file_in_existing_folder_without_opening_by_default(
    calc_function,
    mock_webbrowser_open,
    mock_os_path_exists,
    mock_os_makedirs,
    mock_builtin_open,
):
    test_folder = "test/folder"
    expected_full_path = os.path.join(test_folder, "calc_report.html")

    report_builder = ReportBuilder(calc_function=calc_function)
    report_path = report_builder.save_report(test_folder)

    assert report_path == expected_full_path

    # doesn't create new directory (path exists)
    mock_os_path_exists.assert_called_once_with(test_folder)
    mock_os_makedirs.assert_not_called()

    # doesn't open browser
    mock_webbrowser_open.assert_not_called()

    # writes a new file at the specified path
    mock_builtin_open.assert_called_once_with(expected_full_path, "w")

    # writes the expected html content to the file
    open_handle = mock_builtin_open()
    report_content = open_handle.write.call_args[0][0]
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content


def test_save_report_writes_to_new_file_when_folder_does_not_exist(
    calc_function,
    mock_webbrowser_open,
    mock_os_path_does_not_exist,
    mock_os_makedirs,
    mock_builtin_open,
):
    test_folder = "test/folder"
    expected_full_path = os.path.join(test_folder, "calc_report.html")

    report_builder = ReportBuilder(calc_function=calc_function)
    report_path = report_builder.save_report(test_folder)

    assert report_path == expected_full_path

    # creates new directory (path does not exist)
    mock_os_path_does_not_exist.assert_called_once_with(test_folder)
    mock_os_makedirs.assert_called_once_with(test_folder)

    # doesn't open browser
    mock_webbrowser_open.assert_not_called()

    # writes a new file at the specified path
    mock_builtin_open.assert_called_once_with(expected_full_path, "w")

    # writes the expected html content to the file
    open_handle = mock_builtin_open()
    report_content = open_handle.write.call_args[0][0]
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content


def test_save_report_writes_to_file_in_existing_folder_with_specified_filename(
    calc_function,
    mock_webbrowser_open,
    mock_os_path_exists,
    mock_os_makedirs,
    mock_builtin_open,
):
    test_folder = "test/folder"
    filename = "a_test_file"
    expected_full_path = os.path.join(test_folder, f"{filename}.html")

    report_builder = ReportBuilder(calc_function=calc_function)
    report_path = report_builder.save_report(test_folder, filename=filename)

    assert report_path == expected_full_path

    # doesn't create new directory (path exists)
    mock_os_path_exists.assert_called_once_with(test_folder)
    mock_os_makedirs.assert_not_called()

    # doesn't open browser
    mock_webbrowser_open.assert_not_called()

    # writes a new file at the specified path with specified name
    mock_builtin_open.assert_called_once_with(expected_full_path, "w")

    # writes the expected html content to the file
    open_handle = mock_builtin_open()
    report_content = open_handle.write.call_args[0][0]
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content


def test_save_report_writes_to_file_in_existing_folder_and_opens(
    calc_function,
    mock_webbrowser_open,
    mock_os_path_exists,
    mock_os_makedirs,
    mock_builtin_open,
):
    test_folder = "test/folder"
    expected_full_path = os.path.join(test_folder, "calc_report.html")

    report_builder = ReportBuilder(calc_function=calc_function)
    report_path = report_builder.save_report(test_folder, open_on_save=True)

    assert report_path == expected_full_path

    # doesn't create new directory (path exists)
    mock_os_path_exists.assert_called_once_with(test_folder)
    mock_os_makedirs.assert_not_called()

    # opens file in browser
    mock_webbrowser_open.assert_called_once_with(
        "file://" + os.path.realpath(expected_full_path)
    )

    # writes a new file at the specified path
    mock_builtin_open.assert_called_once_with(expected_full_path, "w")

    # writes the expected html content to the file
    open_handle = mock_builtin_open()
    report_content = open_handle.write.call_args[0][0]
    assert "a =  4 \\ \\mathrm{in}" in report_content
    assert "{\\left( {a} \\right)}^{ {2} } + {a} + {2}" in report_content
    assert "<!DOCTYPE html>" in report_content
    assert '<html style="background-color: #eeeeee;">' in report_content
