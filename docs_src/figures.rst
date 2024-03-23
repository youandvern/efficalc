.. _figures:

Figures in Calc Reports
=======================

Efficalc currently supports three different sources for showing images and figures in your calculation report: raw bytes, files, and matplotlib figures.

If you need to show figures from a different source, `raise an issue <https://github.com/youandvern/efficalc/issues>`_ and let us know!

Here's how a figure will display in your report when you add a caption:

.. image:: /_static/matplotlib_fig.jpg
    :alt: A matplotlib plot displayed in a calculation report
    :align: center


Figure from a file
------------------

To add a saved image file in your calculation report, just add the following :code:`FigureFromFile` object where the file should display in the report.

By supplying the path to your file, :code:`FigureFromFile` will lazy-load the image into the report when it comes time to generate the report.

API docs
********

.. autoclass:: efficalc.FigureFromFile
    :members:


Example
*******

.. code-block:: python
    :linenos:

    def calculation():
        # The start of your calc report

        # Display a figure from my computer in the report
        FigureFromFile(r"C:\Pictures\calculations\calc_image.png")

        # The rest of your calc report


Figure from a matplotlib figure
-------------------------------

`Matplotlib <https://matplotlib.org/>`_ is a popular python library for creating plots and figures. We created :code:`FigureFromMatplotlib` as a simple wrapper around the matplotlib figures to easily integrate them into your calculation reports.

By supplying the matplotlib figure, :code:`FigureFromMatplotlib` will lazy-load the figure into the report when it comes time to generate the report.

API docs
********

.. autoclass:: efficalc.FigureFromMatplotlib
    :members:


Example
*******

.. code-block:: python
    :linenos:

    from matplotlib import pyplot as plt


    def draw_figure_with_matplotlib():
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4])
        return fig


    def calculation():
        # The start of your calc report

        # Draw a figure and display it in the report
        figure = draw_figure_with_matplotlib()
        FigureFromMatplotlib(figure)

        # The rest of your calc report


Figure from raw bytes
---------------------

If you are creating figures a different way and need a more flexible class to display your figures, you can use :code:`FigureFromBytes`.

By supplying the the raw bytes, :code:`FigureFromBytes` will generally require greater resources throughout the calculation process because it is storing the entire figure in memory. This may not be a problem, but if you are running batch calculations or using a lot of figures in your calculation, you may see performance issues.

API docs
********

.. autoclass:: efficalc.FigureFromBytes
    :members:


Example
*******

.. code-block:: python
    :linenos:

    def calculation():
        # The start of your calc report

        # Display a figure from raw bytes in the report
        figure_bytes = generate_figure_bytes()
        FigureFromMatplotlib(figure_bytes)

        # The rest of your calc report

