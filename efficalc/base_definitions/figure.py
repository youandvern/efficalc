import base64
from io import BytesIO
from os import PathLike
from typing import Literal

from .shared import CalculationItem, save_calculation_item

FigureDisplayType = Literal["report-only", "report-input", "report-result"]


class FigureBase(CalculationItem):
    """A base class for displaying figures in a calculation report.

    :param caption: The caption for the figure, defaults to None
    :type caption: str, optional
    :param full_width: Whether the figure should be full width, defaults to False
    :type full_width: bool, optional
    :param display_type: Where the figure should be displayed, defaults to "report-only"
    :type display_type: FigureDisplayType, optional
    """

    def __init__(
        self,
        caption: str = None,
        full_width: bool = False,
        display_type: FigureDisplayType = "report-only",
    ):
        self.caption = caption
        self.full_width = full_width
        self.display_type = display_type
        self._figure_bytes = None
        save_calculation_item(self)

    @property
    def figure_bytes(self) -> bytes:
        """Loads the image data if it hasn't been loaded yet and returns it as bytes"""
        if self._figure_bytes is None:
            self._figure_bytes = self.load_image_data()
        return self._figure_bytes

    def load_image_data(self) -> bytes:
        """Subclasses should override this method to load image data."""
        raise NotImplementedError

    def get_base64_str(self) -> str:
        """Returns the base64 encoded string of the figure"""
        return base64.b64encode(self.figure_bytes).decode("utf-8")


class FigureFromMatplotlib(FigureBase):
    """This displays MatplotLib figures in calculation reports.

    :param figure: The MatplotLib figure object
    :type figure: matplotlib.figure.Figure
    :param caption: The caption for the figure, defaults to None
    :type caption: str, optional
    :param full_width: Whether the figure should be full width, defaults to False
    :type full_width: bool, optional
    """

    def __init__(self, figure, caption: str = None, full_width: bool = False):
        self.figure = figure
        super().__init__(caption, full_width)

    def load_image_data(self) -> bytes:
        """Loads the image data from the Matplotlib figure object as bytes."""
        with BytesIO() as tmp_file:
            self.figure.savefig(tmp_file, format="png")
            return tmp_file.getvalue()


class FigureFromFile(FigureBase):
    """This displays figures from a file source in calculation reports. File type should be
    compatible with html image tags (e.g. .png, .jpg, .svg, .gif, etc.).

    :param file_path: The path to the image file
    :type file_path: str | PathLike
    :param caption: The caption for the figure, defaults to None
    :type caption: str, optional
    :param full_width: Whether the figure should be full width, defaults to False
    :type full_width: bool, optional
    """

    def __init__(
        self, file_path: str | PathLike, caption: str = None, full_width: bool = False
    ):
        self.file_path = file_path
        super().__init__(caption, full_width)

    def load_image_data(self):
        """Loads the image data from the file as bytes."""
        with open(self.file_path, "rb") as file:
            file_bytes = file.read()
        return file_bytes


class FigureFromBytes(FigureBase):
    """This displays figures in calculation reports by directly supplying the figure bytes. Figure
    should be compatible with html image tags (e.g. .png, .jpg, .svg, .gif, etc.).

    :param figure_bytes: The bytes of the image
    :type figure_bytes: bytes
    :param caption: The caption for the figure, defaults to None
    :type caption: str, optional
    :param full_width: Whether the figure should be full width, defaults to False
    :type full_width: bool, optional
    """

    def __init__(
        self, figure_bytes: bytes, caption: str = None, full_width: bool = False
    ):
        self._bytes = figure_bytes
        super().__init__(caption, full_width)

    def load_image_data(self) -> bytes:
        """Loads the image bytes."""
        return self._bytes
