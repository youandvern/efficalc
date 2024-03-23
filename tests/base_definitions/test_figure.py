import pathlib
from typing import IO

import pytest

from efficalc import (
    FigureFromBytes,
    FigureFromFile,
    FigureFromMatplotlib,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
)


class MockMatplotlibFigure:
    format = None

    def __init__(self, content):
        self._content = content

    def savefig(self, file_io: IO, format: str = "png"):
        self.format = format
        file_io.write(self._content)


@pytest.fixture
def common_setup_teardown():
    data = 5  # Set up a sample number
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_all_input_default_overrides()
    clear_saved_objects()


def test_figure_from_file(common_setup_teardown):

    path = pathlib.Path(__file__).parent.resolve()
    file_name = "efficalc.png"
    full_path = path / file_name
    part_of_encoding = "2OzA1J1sWb637gToglEjnquZs+AJIq+Okrcyk01RThbnIxc7znH+y/zHl4toYh3RuY9whn+sxPKENc7pp7917xnRz3vihMWV0Le13nP3tpRtRNSL4i4ce8R81beKZ/37OpaHfeP7YIbj3o/yKq3e9Qcc2MV3vtxi/cvuEXcaFnNOl7l/3WRwx4Tp80+/hoAAAAAbEDQDgApQMDetIwN2lUHu9rcdO7T1m2S21xSEbRXv3a4SMV6Xdkh44S3RHIZyQMAAADAHqrVCQCQJCpYj336K4mNvZSQvQk50c16ZQ51sSY65tLvRg4huFRnum0yC/UCAAAAAOxARzsAJElsztP+eA9GezS9cJ/zJDTkWl0FnOpin3K3xNWYGDS58KhHk77RbvVbJ4hsXqYrO2ScNUWvAACAKT6buV7uf2WeFOREpGVepmRmOBIJOZIRCUkk7D2HQ/46Q623HqtZq9cyM7xHndd3xnFEcjIjkp1Z87W1YnHXe4hEvf/47lkd23mspSKv6pgrVdVxqYrGt1mrR2V1TLZU1jzKKqLec9x7RPXXuP5/x6s3jdR/NwDYNYJ2AEiQ6lxXAXt8+Rh9BE0t1PMkCY+4RVfB5Y8cmnQTHezNKCVB+zunipQs1JX5nOw2EjnpA10BAABTjJ26Tkb/5hNd2WFY70KZ/MBhugKAXWN0DAAkQHWx++M9CNmbV1XA7yJQXeyTbqoZOUTI3rxScEeKv6mpTXLa6AUAADBJZVVMr+zRtmWWXgHA7hG0A0BjVJf6s7PVg1ExSIS6I8K/WMOomPSQios2tgXtkXy9AAAAJlGjVmzTpiBTrwBg9wjaAaChVPfxxJv8bnYgEbUbnrJxruEcu063nMwWegUAAExiY9BORzuAhiBoB4AG8LuP3zubUTFpxg3gXQXqQk3s019xR0SaCeJ7Ke1E8vQCAACYRG0Oahs62gE0BEE7ANSTCtlVMMoMbSRKheyMHYKxMgjaAQAwUWU1M9oBYFcI2gGgHgjZ01yANkPdGrIjPVWV6EUSxaN6YQcng9ExAACYyM7RMdl6BQC7R9AOALtByB4AAekM90P26X"
    fig = FigureFromFile(str(full_path), "efficalc logo", True)
    assert part_of_encoding in fig.get_base64_str()
    assert fig.caption == "efficalc logo"
    assert fig.full_width


def test_figure_from_file_defaults(common_setup_teardown):

    path = pathlib.Path(__file__).parent.resolve()
    file_name = "efficalc.png"
    full_path = path / file_name
    fig = FigureFromFile(str(full_path))
    assert fig.caption is None
    assert not fig.full_width


def test_figure_from_file_saved_as_calc_item(common_setup_teardown):
    path = pathlib.Path(__file__).parent.resolve()
    file_name = "efficalc.png"
    full_path = path / file_name
    fig = FigureFromFile(str(full_path))
    saved_objects = get_all_calc_objects()
    assert len(saved_objects) == 1
    assert saved_objects[0] == fig


def test_figure_from_matplotlib(common_setup_teardown):
    mat_fig = MockMatplotlibFigure(b"test figure")
    fig = FigureFromMatplotlib(mat_fig, "matplotlib plot", True)
    assert "dGVzdCBmaWd1cmU=" == fig.get_base64_str()
    assert fig.caption == "matplotlib plot"
    assert fig.full_width


def test_figure_from_matplotlib_defaults(common_setup_teardown):
    mat_fig = MockMatplotlibFigure(b"test figure")
    fig = FigureFromMatplotlib(mat_fig)
    assert fig.caption is None
    assert not fig.full_width


def test_figure_from_matplotlib_saved_as_calc_item(common_setup_teardown):
    mat_fig = MockMatplotlibFigure(b"test figure")
    fig = FigureFromMatplotlib(mat_fig)
    saved_objects = get_all_calc_objects()
    assert len(saved_objects) == 1
    assert saved_objects[0] == fig


def test_figure_from_bytes(common_setup_teardown):
    fig = FigureFromBytes(b"test figure", "efficalc logo", True)
    assert "dGVzdCBmaWd1cmU=" == fig.get_base64_str()
    assert fig.caption == "efficalc logo"
    assert fig.full_width


def test_figure_from_bytes_defaults(common_setup_teardown):
    fig = FigureFromBytes(b"test figure")
    assert fig.caption is None
    assert not fig.full_width


def test_figure_from_bytes_saved_as_calc_item(common_setup_teardown):
    fig = FigureFromBytes(b"test figure")
    saved_objects = get_all_calc_objects()
    assert len(saved_objects) == 1
    assert saved_objects[0] == fig
