import math
from typing import List, Literal, Optional, Tuple, Union

PlanarPoint = Union[Tuple[float, float], List[float]]
PlanarPoints = Union[List[Tuple[float, float]], List[List[float]]]
MarkerIdType = Literal["arrow", "arrow_reverse", "dot"]


class CanvasElement:
    """
    Base class for SVG elements.

    :param fill: Fill color of the element, defaults to None.
    :param stroke: Stroke color of the element, defaults to None.
    :param stroke_width: Stroke width of the element, defaults to None.
    """

    def __init__(
        self, fill: str = None, stroke: str = None, stroke_width: float = None
    ):
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

    def get_common_svg_style_elements(self) -> str:
        """
        Returns the common style elements for the svg element.
        """
        fill_prop = f' fill="{self.fill}"' if self.fill is not None else ""
        stroke_prop = f' stroke="{self.stroke}"' if self.stroke is not None else ""
        stroke_width_prop = (
            f' stroke-width="{self.stroke_width}"'
            if self.stroke_width is not None
            else ""
        )
        return f"{fill_prop}{stroke_prop}{stroke_width_prop}"

    def to_svg(self) -> str:
        """
        Converts the element to its SVG representation.

        :return: SVG representation of the element.
        """
        raise NotImplementedError("Must be implemented by subclasses")


class Marker(CanvasElement):
    """
    Base class for line and polyline end markers (arrows, circles, etc.)

    :param fill: Fill color of the marker, defaults to "context-stroke". Marker fill can be set to "context-fill"
        or "context-stroke to match the fill or stroke of the element this marker is connected to.
    :param stroke: Stroke color of the marker, defaults to "none". Marker stroke can be set to "context-stroke"
        or "context-fill" to match the fill or stroke of the element this marker is connected to.
    :param stroke_width: Stroke width of the marker, defaults to None.
    :param size: Size scale of the arrow marker relative to the stroke-width, defaults to 1.
    """

    def __init__(
        self,
        fill: str = "context-stroke",
        stroke: str = "none",
        stroke_width: float = None,
        size: float = 1,
    ):

        self.size = size
        super().__init__(fill=fill, stroke=stroke, stroke_width=stroke_width)

    @property
    def id(self) -> str:
        return f"{self.__class__.__name__}-{self.fill}-{self.stroke}-{self.stroke_width}-{self.size}"

    def __eq__(self, other: object) -> bool:
        # Ensure uniqueness based on the dynamic 'id' attribute
        return (self.id == other.id) if isinstance(other, Marker) else False

    def __hash__(self):
        return hash(self.id)  # Use the dynamic 'id' attribute for hashing

    def __repr__(self):
        return self.id


class Rectangle(CanvasElement):
    """
    Represents a rectangle.

    :param x: X coordinate of the top-left corner.
    :param y: Y coordinate of the top-left corner.
    :param width: Width of the rectangle.
    :param height: Height of the rectangle.
    :param rx: Horizontal radius of the corners, defaults to 0.
    :param ry: Vertical radius of the corners, defaults to 0.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rx: Optional[float] = 0,
        ry: Optional[float] = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry

    def to_svg(self) -> str:
        return (
            f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" '
            f'rx="{self.rx}" ry="{self.ry}"{self.get_common_svg_style_elements()} />'
        )


class Circle(CanvasElement):
    """
    Represents a circle.

    :param cx: X coordinate of the circle center.
    :param cy: Y coordinate of the circle center.
    :param r: Radius of the circle.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.
    """

    def __init__(self, cx: float, cy: float, r: float, **kwargs):
        super().__init__(**kwargs)
        self.cx = cx
        self.cy = cy
        self.r = r

    def to_svg(self) -> str:
        return f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.r}" {self.get_common_svg_style_elements()} />'


class Ellipse(CanvasElement):
    """
    Represents an ellipse.

    :param cx: X coordinate of the ellipse center.
    :param cy: Y coordinate of the ellipse center.
    :param rx: X radius of the ellipse.
    :param ry: Y radius of the ellipse.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.
    """

    def __init__(self, cx: float, cy: float, rx: float, ry: float, **kwargs):
        super().__init__(**kwargs)
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry

    def to_svg(self) -> str:
        return f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" {self.get_common_svg_style_elements()} />'


class Line(CanvasElement):
    """
    Represents a line.

    :param x1: X coordinate of the start point.
    :param y1: Y coordinate of the start point.
    :param x2: X coordinate of the end point.
    :param y2: Y coordinate of the end point.
    :param marker_start: Marker to display at the start, defaults to None.
    :param marker_end: Marker to display at the end, defaults to None.
    :param kwargs: Additional properties such as stroke and stroke_width.
    """

    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        marker_start: Marker = None,
        marker_end: Marker = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.marker_start = marker_start
        self.marker_end = marker_end
        self.marker_mid = None

    def to_svg(self) -> str:
        starting_marker = (
            f' marker-start="url(#{self.marker_start.id})"' if self.marker_start else ""
        )
        ending_marker = (
            f' marker-end="url(#{self.marker_end.id})"' if self.marker_end else ""
        )
        return f'<line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" y2="{self.y2}"{starting_marker}{ending_marker}{self.get_common_svg_style_elements()} />'


class Polyline(CanvasElement):
    """
    Represents a polyline with optional corner rounding.

    :param points: A list of (x, y) tuples or lists defining the polyline points,
        i.e. [(0, 0), (50, 50), (100, 0)].
    :param corner_radius: The radius of the rounded corners if >0, defaults to 0.
    :param marker_start: Marker to display at the start, defaults to None.
    :param marker_end: Marker to display at the end, defaults to None.
    :param marker_mid: Marker to display at midpoints, defaults to None.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.

    .. note::
        If the requested radius does not fit for any corner of the polyline,
        that corner will not be rounded at all.
    """

    def __init__(
        self,
        points: PlanarPoints,
        corner_radius: float = 0,
        marker_start: Marker = None,
        marker_end: Marker = None,
        marker_mid: Marker = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.points = points
        self.corner_radius = corner_radius
        self.marker_start = marker_start
        self.marker_end = marker_end
        self.marker_mid = marker_mid

    @classmethod
    def _dist_btn_points(cls, p1: PlanarPoint, p2: PlanarPoint) -> float:
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @classmethod
    def _calc_fillet_points(
        cls,
        prev_pt: PlanarPoint,
        corner_pt: PlanarPoint,
        next_pt: PlanarPoint,
        radius: float,
    ) -> tuple[PlanarPoint, PlanarPoint]:
        """
        Rounds the corner of a polyline by creating a fillet.

        This method calculates the points of a fillet arc that rounds the corner formed
        by `prev_point`, `corner_point`, and `next_point` with a given radius.

        :param prev_pt: The point before the corner point in the polyline.
        :param corner_pt: The corner point of the polyline to be rounded.
        :param next_pt: The point after the corner point in the polyline.
        :param radius: The radius of the fillet to be applied to the corner.
        :return: A tuple containing two points: the start and end points of the fillet arc.

        .. note::
            If the requested fillet radius does not fit within the segment lengths,
            the method will return the original corner point twice, indicating no fillet was applied.
        """

        # Vector from corner to previous point and corner to next point
        prev_vector = (prev_pt[0] - corner_pt[0], prev_pt[1] - corner_pt[1])
        next_vector = (next_pt[0] - corner_pt[0], next_pt[1] - corner_pt[1])

        # Normalize vectors
        prev_len = cls._dist_btn_points(prev_pt, corner_pt)
        next_len = cls._dist_btn_points(corner_pt, next_pt)
        if prev_len == 0 or next_len == 0:
            return corner_pt, corner_pt

        prev_vector = (prev_vector[0] / prev_len, prev_vector[1] / prev_len)
        next_vector = (next_vector[0] / next_len, next_vector[1] / next_len)

        # Calculate the tangent points
        tangent_len = radius / math.tan(
            math.acos(prev_vector[0] * next_vector[0] + prev_vector[1] * next_vector[1])
            / 2
        )

        # Prevent floating point errors from preventing an exact full-length fillet
        tangent_len = round(tangent_len, 10)

        # If the requested fillet doesn't fit, don't round the corner
        if prev_len < tangent_len or next_len < tangent_len:
            return corner_pt, corner_pt

        fillet_start = (
            corner_pt[0] + prev_vector[0] * tangent_len,
            corner_pt[1] + prev_vector[1] * tangent_len,
        )
        fillet_end = (
            corner_pt[0] + next_vector[0] * tangent_len,
            corner_pt[1] + next_vector[1] * tangent_len,
        )

        return fillet_start, fillet_end

    def to_path_commands(self) -> str:
        """
        Converts the polyline to an SVG path command string, applying a corner radius for rounded corners if specified.

        :return: SVG path string representation of the polyline.
        :rtype: str
        """
        if self.corner_radius <= 0:
            # If no fillet radius, simply return the polyline points as an SVG path
            return "M " + " ".join([f"{x},{y}" for x, y in self.points])

        path = []
        last_point_idx = len(self.points) - 1
        for i, corner_pt in enumerate(self.points):
            if i == 0:
                path.append(f"M {corner_pt[0]},{corner_pt[1]}")
            elif i == last_point_idx:
                path.append(f"L {corner_pt[0]},{corner_pt[1]}")
            else:
                prev_pt, next_pt = self.points[i - 1], self.points[i + 1]
                fillet_start, fillet_end = self._calc_fillet_points(
                    prev_pt, corner_pt, next_pt, self.corner_radius
                )

                path.append(f"L {fillet_start[0]},{fillet_start[1]}")

                if fillet_start != fillet_end:
                    large_arc_flag = (
                        0
                        if (corner_pt[0] - prev_pt[0]) * (next_pt[1] - corner_pt[1])
                        - (corner_pt[1] - prev_pt[1]) * (next_pt[0] - corner_pt[0])
                        < 0
                        else 1
                    )
                    path.append(
                        f"A {self.corner_radius},{self.corner_radius} 0 0,{large_arc_flag} {fillet_end[0]},{fillet_end[1]}"
                    )

        return " ".join(path)

    def _get_marker_assignments(self):
        assignments = ""
        if self.marker_start:
            assignments += f' marker-start="url(#{self.marker_start.id})"'
        if self.marker_end:
            assignments += f' marker-end="url(#{self.marker_end.id})"'
        if self.marker_mid:
            assignments += f' marker-mid="url(#{self.marker_mid.id})"'
        return assignments

    def to_svg(self) -> str:
        return f'<path d="{self.to_path_commands()}"{self.get_common_svg_style_elements()}{self._get_marker_assignments()} />'


MarkerOrientation = Union[Literal["auto", "auto-start-reverse"], float]


class ArrowMarker(Marker):
    """
    Creates an arrow marker for a line or polyline.

    :param reverse: Whether the marker direction should be reversed, defaults to False.
    :param orientation: The orientation of the marker, defaults to "auto".
    :param kwargs: Additional properties such as fill, stroke, stroke_width, and size.
    """

    def __init__(
        self, reverse: bool = False, orientation: MarkerOrientation = "auto", **kwargs
    ):
        self.reversed = reverse
        self.orientation = orientation
        super().__init__(**kwargs)

    @property
    def id(self) -> str:
        return f"{self.__class__.__name__}-{self.fill}-{self.stroke}-{self.stroke_width}-{self.size}-{self.reversed}-{self.orientation}"

    def to_svg(self) -> str:
        marker_size = self.size * 4
        stroke_width = self.stroke_width if self.stroke_width is not None else 0
        view_size = marker_size + 2 * stroke_width
        min_position = stroke_width
        max_position = marker_size + min_position
        half_position = view_size / 2

        path = (
            f"M {min_position} {half_position} L {max_position} {min_position} L {max_position} {max_position} z"
            if self.reversed
            else f"M {min_position} {min_position} L {max_position} {half_position} L {min_position} {max_position} z"
        )
        return (
            f'<marker id="{self.id}" viewBox="0 0 {view_size} {view_size}" '
            f'refX="{half_position}" refY="{half_position}" markerUnits="strokeWidth" '
            f'markerWidth="{view_size}" markerHeight="{view_size}" orient="{self.orientation}"><path '
            f'd="{path}" {self.get_common_svg_style_elements()} /></marker>'
        )


class CircleMarker(Marker):
    """
    Creates a circle marker for a line or polyline.

    :param kwargs: Additional properties such as fill, stroke, stroke_width, and size.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_svg(self) -> str:
        stroke_width = self.stroke_width if self.stroke_width is not None else 0
        radius = self.size
        view_size = 2 * radius + stroke_width
        middle = view_size / 2
        return (
            f'<marker id="{self.id}" viewBox="0 0 {view_size} {view_size}" '
            f'refX="{middle}" refY="{middle}" markerUnits="strokeWidth" '
            f'markerWidth="{view_size}" markerHeight="{view_size}"> '
            f'<circle cx="{middle}" cy="{middle}" r="{radius}"{self.get_common_svg_style_elements()} /></marker>'
        )
