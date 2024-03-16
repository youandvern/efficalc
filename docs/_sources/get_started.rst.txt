.. _start:

Quickstart
==========

New releases of efficalc are distributed on PyPI_.

.. _PyPI: https://pypi.org/project/efficalc/

Installation
------------

Install to your project via pip:

.. code-block:: bash

    pip install efficalc


First Calculation Function
--------------------------

Efficalc works best when calculations are defined as a function. The most common classes you'll use are :code:`Input` and :code:`Calculation`.

For example, if you want a calculation for pythagorean's theorem and the perimeter of a right triangle, your calculation may be:

.. code-block:: python
    :linenos:

    from efficalc import Calculation, Input, Title, sqrt


    def calculation():
        Title("Pythagorean's Theorem and Perimeter")

        a = Input("a", 3, description="Length of side a")
        b = Input("b", 4, description="Length of side b")

        c = Calculation("c", sqrt(a**2 + b**2), description="Length of the hypotenuse")

        Calculation("P", a + b + c, description="Perimeter of the triangle")


View Reports
------------

There are a few ways to produce a report for your calculations. To view and print the report from your browser, you can do something as simple as:

.. code-block:: python
    :linenos:

    from efficalc.report_builder import ReportBuilder
    from pythagorean_perimeter import calculation

    builder = ReportBuilder(calculation)
    builder.view_report()

Running this code gives us this nice report:

|pythag_default|

.. |pythag_default| raw:: html

   <iframe src="_static/pythagorean_default.pdf" width="100%" height="500px"></iframe>


.. _change_input_values:

Change Input Values
-------------------

Now that's great and easy, but it will always return the same calculation with the same default inputs that we gave in the :code:`Calculation` function (3 and 4).

But we want to make our calculations flexible so we can use the same function for many different design inputs. Luckily, the :code:`ReportBuilder` makes this super easy by supplying any input overrides to the second argument.

Here's an example:

.. code-block:: python
    :linenos:

    from efficalc.report_builder import ReportBuilder
    from pythagorean_perimeter import calculation

    # define the new inputs to override the defaults
    new_inputs = {"a": 5, "b": 6}

    # run the report with the input override values
    builder = ReportBuilder(calculation, new_inputs)
    builder.view_report()

Now, our report shows the updated inputs. Not the default inputs we defined in the calculation function:

|pythag_update|

.. |pythag_update| raw:: html

   <iframe src="_static/pythagorean_update_input.pdf" width="100%" height="500px"></iframe>


And that's all there is to it!

Well actually there's a lot more that you can do with efficalc.

But the overall pattern is the same no matter how advanced you want to make your calculations. Take a deeper dive into our examples and API documentation to see all of the options we have to build the perfect calculations.

Happy efficalcing!
