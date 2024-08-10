import copy
from typing import List, Literal, Set

from efficalc import CalculationItem, save_calculation_item
from efficalc.canvas.canvas_elements import CanvasElement, ElementWithMarkers, Marker

CanvasDisplayType = Literal["report-only", "report-input", "report-result"]


class Canvas(CalculationItem):
    """
    Represents a canvas to hold and manage multiple SVG elements. This is the backdrop of the drawn figure. Coordinate
    system starts in the top left corner of the canvas with x-axis pointing right and y-axis pointing down.

    :param width: Width of the canvas drawing space.
    :param height: Height of the canvas drawing space.
    :param min_xy: Minimum x and y values of the canvas drawing space, defaults to (0, 0).
    :param caption: Caption for the canvas, defaults to None.
    :param centered: Whether to center the canvas, defaults to True.
    :param full_width: Whether to make the canvas full width, defaults to False.
    :param display_type: Where the canvas should be displayed, defaults to "report-only"
    :param background_color: Background color of the canvas, defaults to "white".
    :param border_width: Width of the border around the canvas, defaults to 0.
    :param border_color: Color of the border around the canvas, defaults to "black".
    :param scale: Scale the display size of the canvas, defaults to 1.
    :param default_element_fill: Default fill color for elements, defaults to "none".
    :param default_element_stroke: Default stroke color for elements, defaults to "black".
    :param default_element_stroke_width: Default stroke width for elements, defaults to 1.
    """

    def __init__(
        self,
        width: float,
        height: float,
        min_xy: tuple[float, float] = (0, 0),
        caption: str = None,
        centered: bool = True,
        full_width: bool = False,
        display_type: CanvasDisplayType = "report-only",
        background_color: str = None,
        border_width: float = None,
        border_color: str = None,
        scale: float = 1.0,
        default_element_fill: str = "none",
        default_element_stroke: str = "black",
        default_element_stroke_width: float = 1,
    ):

        self.width = width
        self.height = height
        self.min_xy = min_xy
        self.elements: List[CanvasElement] = []
        self.caption = caption
        self.centered = centered
        self.full_width = full_width
        self.display_type = display_type
        self.background_color = background_color
        self.border_width = border_width
        self.border_color = border_color
        self.scale = scale
        self.default_fill = default_element_fill
        self.default_stroke = default_element_stroke
        self.default_stroke_width = default_element_stroke_width
        save_calculation_item(self)

    @classmethod
    def _process_markers(cls, element: CanvasElement) -> list[Marker]:
        """
        Get formatted markers from an element if it includes them.

        :param element: The element to get markers from.
        """

        return element.get_markers() if isinstance(element, ElementWithMarkers) else []

    def _set_defaults(self, element: CanvasElement):
        """
        Sets default values for an element if they are not already set.
        :param element: The element to set defaults for.

        .. note::
            This method modifies the element in place.
        """
        if element.fill is None:
            element.fill = self.default_fill
        if element.stroke is None:
            element.stroke = self.default_stroke
        if element.stroke_width is None:
            element.stroke_width = self.default_stroke_width

    @classmethod
    def _generate_marker_defs(cls, markers: Set[Marker]) -> str:
        """
        Generates marker definitions for the canvas.
        """
        if not markers:
            return ""

        marker_elements = "\n".join([marker.to_svg() for marker in markers])
        return f"<defs>{marker_elements}</defs>"

    def add(self, element: CanvasElement) -> None:
        """
        Adds an element to the canvas.

        :param element: The element to be added.
        """
        self.elements.append(element)

    def to_svg(self) -> str:
        """
        Converts the canvas and its elements to their SVG representation.

        :return: SVG representation of the canvas.
        """
        processed_elements = []
        included_markers: Set[Marker] = set()

        for element in self.elements:
            copied_element = copy.deepcopy(element)
            self._set_defaults(copied_element)
            markers = self._process_markers(copied_element)
            processed_elements.append(copied_element)
            included_markers.update(markers)

        style = "max-width: 100%; display: block;"
        style += (
            " width: 100%;"
            if self.full_width
            else f" width: {self.width * self.scale}px;"
        )
        style += " margin-inline: auto;" if self.centered else ""
        style += (
            f" background-color: {self.background_color};"
            if self.background_color
            else ""
        )
        style += (
            f" border: {self.border_width}px solid {self.border_color};"
            if self.border_color and self.border_width
            else ""
        )

        elements_svg = "\n".join([element.to_svg() for element in processed_elements])
        min_x, min_y = self.min_xy
        return (
            f'<svg viewbox="{min_x} {min_y} {self.width} {self.height}" style="{style}" xmlns="http://www.w3.org/2000/svg">\n'
            f"{self._generate_marker_defs(included_markers)} {elements_svg}"
            f"\n </svg>"
        )
