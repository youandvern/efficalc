import dataclasses

from .shared import CalculationItem, save_calculation_item


@dataclasses.dataclass
class Circle(object):
    """A circle element to be drawn on the canvas.

    :param x: The x coordinate of the circle center
    :type x: int
    :param y: The y coordinate of the circle center
    :type y: int
    :param radius: The radius of the circle
    :type radius: int
    :param stroke: The stroke width of the circle outline. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke: int, optional
    :param stroke_color: The stroke color of the circle. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke_color: str, optional
    :param fill_color: The fill color of the circle, defaults to None
    :type fill_color: str, optional
    """

    x: int
    y: int
    radius: int
    stroke: int = None
    stroke_color: str = None
    fill_color: str = None


@dataclasses.dataclass
class Rectangle(object):
    """A rectangular element to be drawn on the canvas.

    :param x: The x coordinate of the rectangle top left corner
    :type x: int
    :param y: The y coordinate of the rectangle top left corner
    :type y: int
    :param width: The width of the rectangle
    :type width: int
    :param height: The height of the rectangle
    :type height: int
    :param stroke: The stroke width of the rectangle outline. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke: int, optional
    :param stroke_color: The stroke color of the rectangle outline. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke_color: str, optional
    :param fill_color: The fill color of the rectangle, defaults to None
    :type fill_color: str, optional
    """

    x: int
    y: int
    width: int
    height: int
    stroke: int = None
    stroke_color: str = None
    fill_color: str = None


@dataclasses.dataclass
class Line(object):
    """A line element to be drawn on the canvas.

    :param x1: The x coordinate of the line start
    :type x1: int
    :param y1: The y coordinate of the line start
    :type y1: int
    :param x2: The x coordinate of the line end
    :type x2: int
    :param y2: The y coordinate of the line end
    :type y2: int
    :param stroke: The stroke width of the line. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke: int, optional
    :param stroke_color: The stroke color of the line. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke_color: str, optional
    """

    x1: int
    y1: int
    x2: int
    y2: int
    stroke: int = None
    stroke_color: str = None


@dataclasses.dataclass
class Arc(object):
    """An arc element to be drawn on the canvas.

    :param x: The x coordinate of the arc center
    :type x: int
    :param y: The y coordinate of the arc center
    :type y: int
    :param radius: The radius of the arc
    :type radius: int
    :param start_angle: The start angle of the arc
    :type start_angle: int
    :param end_angle: The end angle of the arc
    :type end_angle: int
    :param stroke: The stroke width of the arc outline. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke: int, optional
    :param stroke_color: The stroke color of the arc outline. When set to None, defaults to the canvas default stroke
    properties, defaults to None
    :type stroke_color: str, optional
    :param fill_color: The fill color of the arc, defaults to None
    :type fill_color: str, optional
    """

    x: int
    y: int
    radius: int
    start_angle: int
    end_angle: int
    stroke: int = None
    stroke_color: str = None
    fill_color: str = None


@dataclasses.dataclass
class Text(object):
    """A text element to be drawn on the canvas.

    :param x: The x coordinate of the text
    :type x: int
    :param y: The y coordinate of the text
    :type y: int
    :param text: The text to be drawn
    :type text: str
    :param font_size: The font size of the text, defaults to 12
    :type font_size: int, optional
    :param color: The color of the text. When set to None, defaults to the canvas default stroke color, defaults to None
    :type color: str, optional
    :param align: The alignment of the text, defaults to "center"
    :type align: "center" | "left" | "right", optional
    """

    x: int
    y: int
    text: str
    font_size: int = 12
    color = None
    align: str = "center"


class Canvas(CalculationItem):
    """A Python wrapper for drawing with html canvas elements.

    :param width: The width of the canvas, defaults to 300 px
    :type width: int, optional
    :param height: The height of the canvas, defaults to 300 px
    :type height: int, optional
    :param default_stroke_width: The default stroke width of the elements on the canvas, defaults to 1
    :type default_stroke_width: int, optional
    :param default_stroke_color: The default stroke color of the elements on the canvas, defaults to #000000
    :type default_stroke_color: str, optional
    :param background_color: The background color of the canvas, defaults to None
    :type background_color: str, optional
    :param outline_color: The outline color of the canvas, defaults to None
    :type outline_color: str, optional
    :param outline_stroke_width: The outline stroke width of the canvas, defaults to None
    :type outline_stroke_width: int, optional
    """

    def __init__(
        self,
        width: int = 300,
        height: int = 300,
        default_stroke_width: int = 1,
        default_stroke_color: str = "#000000",
        background_color: str = None,
        outline_color: str = None,
        outline_stroke_width: int = None,
    ):
        self.width = width
        self.height = height
        self.default_stroke_width = default_stroke_width
        self.default_stroke_color = default_stroke_color
        self.background_color = background_color
        self.outline_color = outline_color
        self.outline_stroke_width = outline_stroke_width
        self._elements = []
        save_calculation_item(self)

    def add_element(self, element):
        self._elements.append(element)

    def add_elements(self, elements: list[Circle | Rectangle]):
        self._elements.extend(elements)

    def get_elements(self):
        return self._elements
