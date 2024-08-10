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


class ElementWithMarkers(CanvasElement):
    """
    Base class for elements with markers. Subclasses must implement the _get_markers method.
    """

    def _get_markers(self) -> List[Marker]:
        """
        Returns a list of all unformatted markers contained by the element.
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def get_markers(self) -> list[Marker]:
        """
        Returns a list of all markers contained by the element with formatting applied.
        """
        markers = self._get_markers()
        for marker in markers:
            self._apply_context_marker_styles(marker)
        return markers

    def _apply_context_marker_styles(self, marker: Marker) -> Marker:
        """
        Applies context fill and stroke to marker if they are set to "context-fill" or "context-stroke".
        :param marker: The marker to apply context fill and stroke to if context styles are requested.

        """
        if marker.fill == "context-fill":
            marker.fill = self.fill
        if marker.stroke == "context-stroke":
            marker.stroke = self.stroke

        return marker


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


class Line(ElementWithMarkers):
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

    def _get_markers(self) -> List[Marker]:
        markers = []
        if self.marker_start:
            markers.append(self.marker_start)
        if self.marker_end:
            markers.append(self.marker_end)
        return markers

    def to_svg(self) -> str:
        starting_marker = (
            f' marker-start="url(#{self.marker_start.id})"' if self.marker_start else ""
        )
        ending_marker = (
            f' marker-end="url(#{self.marker_end.id})"' if self.marker_end else ""
        )
        return f'<line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" y2="{self.y2}"{starting_marker}{ending_marker}{self.get_common_svg_style_elements()} />'


class Polyline(ElementWithMarkers):
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

    def _get_markers(self) -> List[Marker]:
        markers = []
        if self.marker_start:
            markers.append(self.marker_start)
        if self.marker_end:
            markers.append(self.marker_end)
        if self.marker_mid:
            markers.append(self.marker_mid)
        return markers

    def to_svg(self) -> str:
        return f'<path d="{self.to_path_commands()}"{self.get_common_svg_style_elements()}{self._get_marker_assignments()} />'


class Text(CanvasElement):
    """
    Represents a text element in the canvas.

    :param text: The text content to be rendered.
    :param x: The x-coordinate of the text base point.
    :param y: The y-coordinate of the text base point.
    :param font_size: The font size of the text.
    :param rotate: The rotation angle of the text about the base point (clockwise in degrees).
    :param horizontal_base: The horizontal base point location of the text.
    :param vertical_base: The vertical base point location of the text.
    :param fill: The fill color of the text.
    :param stroke: The stroke color of the text.
    :param stroke_width: The stroke width of the text.
    """

    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        font_size: float | str = "auto",
        rotate: float = 0,
        horizontal_base: Literal["start", "center", "end"] = "start",
        vertical_base: Literal["auto", "top", "middle", "bottom"] = "auto",
        fill: str = "black",
        stroke: str = "none",
        stroke_width: float = 0,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.rotate = rotate
        self.horizontal_base = horizontal_base
        self.vertical_base = vertical_base

        super().__init__(fill=fill, stroke=stroke, stroke_width=stroke_width)

    def _get_horizontal_base_prop(self) -> str:
        default_text_anchor = "start"
        horizontal_base_to_text_anchor = {
            "start": "start",
            "center": "middle",
            "end": "end",
        }
        if (
            self.horizontal_base == default_text_anchor
            or self.horizontal_base not in horizontal_base_to_text_anchor
        ):
            return ""
        return f' text-anchor="{horizontal_base_to_text_anchor[self.horizontal_base]}"'

    def _get_vertical_base_prop(self) -> str:
        default_dominant_baseline = "auto"
        vertical_base_to_dominant_baseline = {
            "auto": "auto",
            "top": "hanging",
            "middle": "middle",
            "bottom": "text-top",
        }
        if (
            self.vertical_base == default_dominant_baseline
            or self.vertical_base not in vertical_base_to_dominant_baseline
        ):
            return ""
        return f' dominant-baseline="{vertical_base_to_dominant_baseline[self.vertical_base]}"'

    def to_svg(self) -> str:
        rotate = f' transform="translate({self.x}, {self.y}) rotate({self.rotate})"'
        font_size = "" if self.font_size == "auto" else f' font-size="{self.font_size}"'
        return (
            f'<text x="0" y="0"{rotate}{font_size}{self.get_common_svg_style_elements()}'
            f"{self._get_horizontal_base_prop()}{self._get_vertical_base_prop()}>{self.text}</text>"
        )


class Dimension(ElementWithMarkers):
    """
    Represents a dimension line between two points.

    :param x1: X coordinate of the start point.
    :param y1: Y coordinate of the start point.
    :param x2: X coordinate of the end point.
    :param y2: Y coordinate of the end point.
    :param text: The text to display as the dimension, defaults to the length of the dimension line.
    :param gap: The gap between the points being dimensioned and the start of the extension lines, defaults to 2.
    :param offset: Offset distance from the parallel dimension line to the dimensioned points. Positive offset will
        result in the dimension extending upward, negative offset will result in the dimension extending downward.
        Defaults to 10.
    :param unit: The unit of the dimension, defaults to None.
    :param text_position: The position of the text relative to the dimension line. Defaults to 'top'.
    :param text_size: Scaling factor for text size. Defaults to 1.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.
    """

    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        text: Optional[str] = None,
        gap: float = 0,
        offset: float = 10,
        unit: Optional[str] = None,
        text_position: Literal["top", "bottom"] = "top",
        text_size: float = 1.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        normalize_direction = x1 > x2
        self.x1 = x2 if normalize_direction else x1
        self.y1 = y2 if normalize_direction else y1
        self.x2 = x1 if normalize_direction else x2
        self.y2 = y1 if normalize_direction else y2
        self.text = text
        self.gap = gap
        self.offset = offset
        self.unit = unit
        self.text_position = text_position
        self.text_size = text_size
        self.additional_props = kwargs

    def _calc_length(self) -> float:
        return math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

    @staticmethod
    def _calc_unit_vector(
        x1: float, y1: float, x2: float, y2: float
    ) -> tuple[float, float]:
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx**2 + dy**2)
        return dx / length, dy / length

    def _calc_perpendicular_vector(self) -> tuple[float, float]:
        # Calculate direction vector for dimension line
        ux, uy = self._calc_unit_vector(self.x1, self.y1, self.x2, self.y2)

        # Return perpendicular vector for offset
        return -uy, ux

    @property
    def _stroke_width(self) -> float:
        return self.stroke_width or 1

    @property
    def _scaled_offset(self) -> float:
        return self.offset * -1

    def _get_dimension_line(self) -> Line:
        offset = self._scaled_offset
        perp_ux, perp_uy = self._calc_perpendicular_vector()
        marker_start = ArrowMarker(orientation="auto-start-reverse", base="point")
        marker_end = ArrowMarker(base="point")
        # Calculate dimension line points
        d1_x, d1_y = self.x1 + offset * perp_ux, self.y1 + offset * perp_uy
        d2_x, d2_y = self.x2 + offset * perp_ux, self.y2 + offset * perp_uy
        return Line(
            x1=d1_x,
            y1=d1_y,
            x2=d2_x,
            y2=d2_y,
            marker_start=marker_start,
            marker_end=marker_end,
            stroke=self.stroke,
            stroke_width=self._stroke_width,
        )

    def _get_markers(self) -> List[Marker]:
        return self._get_dimension_line().get_markers()

    def to_svg(self) -> str:
        perp_ux, perp_uy = self._calc_perpendicular_vector()
        stroke_width = self._stroke_width
        offset = self._scaled_offset
        offset_sign = -1 if offset < 0 else 1

        # Calculate points for extension lines
        gap = self.gap * offset_sign
        ex1_x_start, ex1_y_start = self.x1 + gap * perp_ux, self.y1 + gap * perp_uy
        ex2_x_start, ex2_y_start = self.x2 + gap * perp_ux, self.y2 + gap * perp_uy

        ext_len = offset + stroke_width * 4 * offset_sign
        ex1_x_end, ex1_y_end = self.x1 + ext_len * perp_ux, self.y1 + ext_len * perp_uy
        ex2_x_end, ex2_y_end = self.x2 + ext_len * perp_ux, self.y2 + ext_len * perp_uy

        dimension_line = self._get_dimension_line()

        # Calculate position for dimension text
        text_offset_sign = -1 if self.text_position == "top" else 1
        text_gap = 2 * stroke_width * text_offset_sign
        dim_x1, dim_y1 = dimension_line.x1, dimension_line.y1
        dim_x2, dim_y2 = dimension_line.x2, dimension_line.y2
        text_x = (dim_x1 + dim_x2) / 2 + text_gap * perp_ux
        text_y = (dim_y1 + dim_y2) / 2 + text_gap * perp_uy

        # Calculate rotation angle for dimension text
        ux, uy = self._calc_unit_vector(dim_x1, dim_y1, dim_x2, dim_y2)
        angle_rad = math.atan2(uy, ux)
        text_rotation = math.degrees(angle_rad)

        # Use provided text or default to length
        dimension_text = (
            self.text if self.text is not None else f"{self._calc_length():.2f}"
        )

        # Create SVG elements with scaling
        extension_line1 = Line(
            x1=ex1_x_start,
            y1=ex1_y_start,
            x2=ex1_x_end,
            y2=ex1_y_end,
            stroke=self.stroke,
            stroke_width=stroke_width,
        )
        extension_line2 = Line(
            x1=ex2_x_start,
            y1=ex2_y_start,
            x2=ex2_x_end,
            y2=ex2_y_end,
            stroke=self.stroke,
            stroke_width=stroke_width,
        )
        text_element = Text(
            text=(
                f"{dimension_text}{self.unit}"
                if self.unit is not None
                else dimension_text
            ),
            x=text_x,
            y=text_y,
            rotate=text_rotation,
            font_size=stroke_width * 7 * self.text_size,
            horizontal_base="center",
            vertical_base="bottom" if self.text_position == "top" else "top",
            fill=self.stroke,
        )

        # Combine SVG elements into one group
        svg_elements = (
            extension_line1.to_svg()
            + extension_line2.to_svg()
            + dimension_line.to_svg()
            + text_element.to_svg()
        )
        return f"<g>{svg_elements}</g>"


class Leader(ElementWithMarkers):
    """
    Represents a leader text with a polyline leader.

    :param marker_x: X coordinate of the marker point.
    :param marker_y: Y coordinate of the marker point.
    :param text_x: X coordinate of the text position.
    :param text_y: Y coordinate of the text position.
    :param text: The text content to display.
    :param marker: The marker at the end of the leader, defaults to None.
    :param landing_len: The length of the landing line.
    :param direction: Relative position of the text in relationship to the landing line ('right' or 'left').
    :param text_size: Scaling factor for text size. Defaults to 1.
    :param kwargs: Additional properties such as fill, stroke, and stroke_width.
    """

    def __init__(
        self,
        marker_x: float,
        marker_y: float,
        text_x: float,
        text_y: float,
        text: str,
        marker: Marker = None,
        landing_len: float = 5,
        direction: Literal["right", "left"] = "right",
        text_size: float = 1.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.marker_x = marker_x
        self.marker_y = marker_y
        self.text_x = text_x
        self.text_y = text_y
        self.text = text
        self.marker = marker
        self.landing_distance = landing_len
        self.direction = direction
        self.text_size = text_size
        self.additional_props = kwargs

    @property
    def _stroke_width(self) -> float:
        return self.stroke_width or 1

    def _get_leader_line(self) -> Polyline:
        direction = -1 if self.direction == "right" else 1
        leader_gap = direction * 2 * self._stroke_width
        points = [
            (self.text_x + leader_gap, self.text_y),
            (self.text_x + direction * self.landing_distance + leader_gap, self.text_y),
            (self.marker_x, self.marker_y),
        ]
        return Polyline(
            points=points,
            marker_end=self.marker,
            stroke=self.stroke,
            stroke_width=self._stroke_width,
            fill="none",
        )

    def _get_markers(self) -> List[Marker]:
        return self._get_leader_line().get_markers()

    def to_svg(self) -> str:
        leader_line = self._get_leader_line()

        text_element = Text(
            text=self.text,
            x=self.text_x,
            y=self.text_y,
            font_size=7 * self._stroke_width * self.text_size,
            horizontal_base="start" if self.direction == "right" else "end",
            vertical_base="middle",
            fill=self.stroke,
        )

        svg_elements = leader_line.to_svg() + text_element.to_svg()
        return f"<g>{svg_elements}</g>"


MarkerOrientation = Union[Literal["auto", "auto-start-reverse"], float]


class ArrowMarker(Marker):
    """
    Creates an arrow marker for a line or polyline.

    :param reverse: Whether the marker direction should be reversed, defaults to False.
    :param orientation: The orientation of the marker, defaults to "auto".
    :param kwargs: Additional properties such as fill, stroke, stroke_width, and size.
    """

    def __init__(
        self,
        reverse: bool = False,
        orientation: MarkerOrientation = "auto",
        base: Literal["point", "center", "flat"] = "center",
        **kwargs,
    ):
        self.reversed = reverse
        self.orientation = orientation
        self.base_point = base
        super().__init__(**kwargs)

    @property
    def id(self) -> str:
        return f"{self.__class__.__name__}-{self.fill}-{self.stroke}-{self.stroke_width}-{self.size}-{self.reversed}-{self.orientation}-{self.base_point}"

    @property
    def marker_size(self) -> float:
        return self.size * 4

    def to_svg(self) -> str:
        marker_size = self.marker_size
        stroke_width = self.stroke_width if self.stroke_width is not None else 0
        view_size = marker_size + 2 * stroke_width
        min_position = stroke_width
        max_position = marker_size + min_position
        half_position = view_size / 2
        ref_x = (
            half_position
            if self.base_point == "center"
            else 0 if self.base_point == "flat" else view_size
        )

        path = (
            f"M {min_position} {half_position} L {max_position} {min_position} L {max_position} {max_position} z"
            if self.reversed
            else f"M {min_position} {min_position} L {max_position} {half_position} L {min_position} {max_position} z"
        )
        return (
            f'<marker id="{self.id}" viewBox="0 0 {view_size} {view_size}" '
            f'refX="{ref_x}" refY="{half_position}" markerUnits="strokeWidth" '
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
