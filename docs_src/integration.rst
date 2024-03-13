.. _integration:

Integrating and Extending efficalc
==================================

Efficalc is designed to be a great standalone resource for building the perfect calculations. But we also appreciate the huge ecosystem of other helpful Python libraries that could work in conjunction with efficalc.

Not to mention the variety of modern workflows that engineers are coming up with everyday.

Here are some ideas and concepts that may help you integrate efficalc with your design workflows or extend the power of efficalc with your favorite libraries.

Parameters and Return Values in Calc Functions
----------------------------------------------

Efficalc is designed to simplify the creation of calculations by eliminating the necessity for parameters or return values. This approach is intended to make building calculations as easy as possible.

However, there might be scenarios where incorporating parameters as input values or producing output from your calculations is necessary to enable other workflows.

In this case, it's best to provide a default value for each argument.

For example, if we want to calculate the hypotenuse of a right triangle, our calculation could look like this:

    .. code-block:: python
        :linenos:

        def pythagorean_with_params(default_a=3, default_b=4):
            a = Input("a", default_a)
            b = Input("b", default_b)
            c = Calculation("c", sqrt(a**2 + b**2), description="Length of the hypotenuse")
            return c.result()

When running the :code:`ReportBuilder`, this is equivalent to:

    .. code-block:: python
        :linenos:

        def pythagorean_without_params():
            a = Input("a", 3)
            b = Input("b", 4)
            c = Calculation("c", sqrt(a**2 + b**2), description="Length of the hypotenuse")

But, the calculation function with input parameters and a return value can also be used just like any other python function:

    .. code-block:: python

        >>> print(pythagorean_with_params())
            5
        >>> print(pythagorean_with_params(5, 6))
            7.810249675906654

With the :code:`ReportBuilder`, we can still update our inputs just the same as shown in :ref:`change_input_values`.


Hundreds of Calculations with One Function
------------------------------------------

Here we'll see a simple example of how one calculation function can be used to design hundreds of beams, columns, or whatever else you're calculating. This really highlights the power of Python over other solutions like Excel.

In this example we will have one calculation and a collection of many inputs. The result will be a design for every input in the collection.

As a bonus, fixing an error in your calculation function will also fix the report and results for all designs that are based on that function.

For this example, we'll use a calculation function with input parameters (see above).

Here's a simplified example that finds the most efficient beam size for a set of constraints:

    .. code-block:: python
        :linenos:


        # Define a calc function for both optimization and the final report
        def beam_strength(default_size="W10X12", default_span=12, default_Fy=50):
            Title("Beam Design")

            # define inputs
            section_size = Input("size", default_size)
            span = Input("span", default_span, "ft")
            Fy = Input("F_y", default_Fy, "ksi")

            # get the section properties for the section size
            size_name = section_size.get_value()
            section = get_aisc_wide_flange(size_name)
            Zx = Calculation("Z_x", section.Zx, "in^3")

            # calculate the strength (more complex in real life)
            strength = Calculation("M_p", Fy * Zx, "k-in")

            # return information about this design for the optimization
            return {
                "size": size_name,
                "weight": section.W,
                "moment_strength": strength.result(),
            }


        # now define an optimization function that uses beam_strength to find the optimal section size
        def find_lightest_beam_for_demand(size_options, moment_demand):
            lightest_beam = {"size": "none", "weight": 999999, "moment_strength": 0}

            # loop through all available sizes
            for size in size_options:

                # run the design calculation to get the strength of the section size
                strength_info = beam_strength(size)
                size_is_strong_enough = strength_info["moment_strength"] > moment_demand
                size_is_lighter_than_best = strength_info["weight"] < lightest_beam["weight"]

                # save the design output for this size if it's better than our previously saved section
                if size_is_strong_enough and size_is_lighter_than_best:
                    lightest_beam = strength_info

            # return the most efficient option we found
            return lightest_beam["size"]


        # only some beam sizes may be available for a certain project, we want to find the most efficient one
        available_beam_sections = [
            "W12X30",
            "W12X26",
            "W12X19",
            "W12X14",
            "W10X49",
            "W10X33",
            "W10X19",
            "W10X12",
            "W8X40",
            "W8X21",
            "W8X15",
        ]

        moment_demand_on_beam = 1000  # k-in
        lightest_beam_size = find_lightest_beam_for_demand(
            available_beam_sections, moment_demand_on_beam
        )

        # view calculation report for the lightest beam
        builder = ReportBuilder(beam_strength, {"size": lightest_beam_size})
        builder.view_report()


That was a lot to digest, but in summary this code:

#. Defined a beam strength calculation function :code:`beam_strength`
#. Defined an optimization function (:code:`find_lightest_beam_for_demand`) that uses the :code:`beam_strength` calculation to find the lightest beam that is strong enough for the given demand
#. Found the lightest available beam shape (by calling :code:`find_lightest_beam_for_demand`)
#. Generated the calculation report for our efficiently designed beam


Helper Functions
----------------

Sometimes you may want to write helper functions that can be shared between multiple calculation functions. Or extracting a helper function might just help your calculation function be more clear and readable.

Helper functions can be utilized within calculations in 2 different ways:

Invisible Helpers
*****************
These functions do not contain any efficalc calculation objects. Using this type of helper function will not show anything extra in a calculation report.

In this example:

    .. code-block:: python
        :linenos:

        def invisible_square_sum(a: float, b: float):
            return (a + b)**2

        def calculation():
            a = Input("a", 3)
            b = Input("b", 4)
            Calculation("c", invisible_square_sum(a.value, b.value), description="An invisible result")

The calculation of variable "c" in this calculation report will simply show:

.. code-block::

        An invisible result
        c = 49


Calculation Helpers
*******************

These functions do contain efficalc calculation objects, so when you use this helper in a calculation function, the efficalc calculation objects within the function will be integrated into the calculation report.

In this example:

    .. code-block:: python
        :linenos:

        def calculate_square_sum(a: Input | Calculation, b: Input | Calculation):
            s = Calculation("sum", a + b)
            return s**2


        def calculation():
            a = Input("a", 3)
            b = Input("b", 4)
            Calculation("c", calculate_square_sum(a, b), description="A calculated result")

The calculation of variable "c" in this calculation report will now show:

.. code-block::

        sum = a + b = 3 + 4
            ∴ sum = 7

        A calculated result
        c = (sum)² = (7)²
          ∴ c = 49


More coming soon
----------------

Request a feature in issues: https://github.com/youandvern/efficalc/issues

Or, feel free to propose an addition to efficalc through a new pull request: https://github.com/youandvern/efficalc/pulls

Here are some ideas we've been thinking about:

- Graphs and Figures
- Matrices
- Tables
- Calculation report for batch calculations (detailed vs. summary)
- Excel plugin integration