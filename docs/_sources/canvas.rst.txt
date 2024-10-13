.. _canvas:

Drawing on a Canvas
===================

Well-written hand-calcs usually have helpful drawings and graphics to illustrate important aspects of the geometry or calculation. That's where a :code:`Canvas` comes in!

The Canvas class allows you to programmatically draw out any part of your calculation and include the graphic in your calculation report.

Examples
--------

Here are some examples of things you may need to draw:

Concrete beam cross-section
***************************

.. image:: /_static/concrete_beam_section.png
    :alt: A reinforced concrete beam section
    :align: center

The source code that generated this image:

.. code-block:: python
    :linenos:

    # Define beam geometry
    width = 10
    height = 16

    # Define reinforcement properties
    cover = 1.5
    num_long_bars = 4
    long_bar_radius = 0.875 / 2
    stirrup_diameter = 0.375
    stirrup_bend_radius = 3 * stirrup_diameter
    stirrup_hook = 3 * stirrup_diameter

    # Set up the canvas
    canvas = Canvas(width, height, caption="Concrete Beam Section", scale=30, default_element_stroke_width=0)

    # Draw the beam outline
    beam_outline = Rectangle(0, 0, width, height, fill="#bdbdbd")
    canvas.add(beam_outline)

    # Add some stirrups for transverse reinforcement (with hooks)
    stirrups = Polyline(
        points=[
            (cover + stirrup_hook, cover + stirrup_hook + stirrup_bend_radius * 1.3),
            (cover, cover + stirrup_bend_radius * 1.3),
            (cover, cover),
            (cover + stirrup_hook, cover),
            (width - cover, cover),
            (width - cover, height - cover),
            (cover, height - cover),
            (cover, cover + stirrup_hook),
            (cover, cover),
            (cover + stirrup_bend_radius * 1.3, cover),
            (cover + stirrup_hook + stirrup_bend_radius * 1.3, cover + stirrup_hook),
        ],
        corner_radius=stirrup_bend_radius,
        stroke_width=stirrup_diameter,
        stroke="black",
    )
    canvas.add(stirrups)

    # Add longitudinal reinforcement (blue circles)
    long_bar_starting_x = cover + stirrup_diameter + long_bar_radius
    long_bar_spacing = (width - 2 * long_bar_starting_x) / (num_long_bars - 1)
    long_bar_y = height - cover - stirrup_diameter / 2 - long_bar_radius

    for i in range(num_long_bars):
        canvas.add(
            Circle(
                long_bar_starting_x + i * long_bar_spacing,
                long_bar_y,
                long_bar_radius,
                fill="#004aad",
            )
        )

    # Add placement bars for transverse reinforcement
    placement_bar = cover + stirrup_diameter * 1.5
    canvas.add(Circle(placement_bar, placement_bar, stirrup_diameter / 2, fill="black"))
    canvas.add(Circle(width - placement_bar, placement_bar, stirrup_diameter / 2, fill="black"))


Beam support and loading scheme
*******************************

.. image:: /_static/beam_loading_canvas.png
    :alt: Beam geometry, supports, and loading
    :align: center

The source code that generated this image:

.. code-block:: python
    :linenos:

    red = "#bf211e"

    # Helper function to draw a pin support at a given location
    def create_pin_support(x, y):
        return Polyline(
            points=[(x, y), (x + 1, y + 2), (x - 1, y + 2), (x, y)],
            stroke_width=0,
            fill="#004aad",
        )

    # Helper function to draw a loading arrow
    def create_load_arrow(x, y, height):
        return Line(
            x, y - height, x, y, stroke_width=0.25, stroke=red, marker_end=ArrowMarker()
        )

    # Helper function to draw a cap line
    def create_load_cap_line(x1, x2, y):
        return Line(x1, y, x2, y, stroke_width=0.25, stroke=red)

    # Set up the canvas
    canvas = Canvas(
        100,
        20,
        caption="Beam geometry, supports, and loading",
        full_width=True,
    )

    # Draw the beam
    canvas.add(Rectangle(20, 13, 60, 2, stroke_width=0.5, fill="#bdbdbd"))

    # Draw the supports
    canvas.add(create_pin_support(20, 15))
    canvas.add(create_pin_support(40, 15))
    canvas.add(create_pin_support(60, 15))
    canvas.add(create_pin_support(80, 15))

    # Draw the arrows for the loading diagram
    arrow_count_per_section = 6
    spacing = 20 / (arrow_count_per_section - 1)
    for i in range(arrow_count_per_section):
        canvas.add(create_load_arrow(20 + spacing * i, 12, 4))
        canvas.add(create_load_arrow(40 + spacing * i, 12, 7))
        canvas.add(create_load_arrow(60 + spacing * i, 12, 4))

    # Draw the cap lines for the loading diagram
    canvas.add(create_load_cap_line(20, 40, 8))
    canvas.add(create_load_cap_line(40, 60, 5))
    canvas.add(create_load_cap_line(60, 80, 8))


API docs
--------

Canvas
******

.. autoclass:: efficalc.canvas.Canvas
    :members:

Canvas Elements
***************

.. autoclass:: efficalc.canvas.Circle
    :members:

.. autoclass:: efficalc.canvas.Ellipse
    :members:

.. autoclass:: efficalc.canvas.Line
    :members:

.. autoclass:: efficalc.canvas.Polyline
    :members:

.. autoclass:: efficalc.canvas.Rectangle
    :members:

.. autoclass:: efficalc.canvas.Text
    :members:

.. autoclass:: efficalc.canvas.Dimension
    :members:

.. autoclass:: efficalc.canvas.Leader
    :members:

Line/Polyline Markers
*********************

.. autoclass:: efficalc.canvas.ArrowMarker
    :members:

.. autoclass:: efficalc.canvas.CircleMarker
    :members:

Base Classes
************

.. autoclass:: efficalc.canvas.CanvasElement
    :members:

.. autoclass:: efficalc.canvas.Marker
    :members:

.. autoclass:: efficalc.canvas.ElementWithMarkers
    :members:

