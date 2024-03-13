.. _testing:

Testing Your Calculations
=========================

    "To err is human, but to really foul things up you need a computer."

    \- Paul R. Ehrlich

The tolerance for mistakes is slim in engineering. But as our industry becomes more digital, the opportunities for large mistakes are increasing.

When we use one spreadsheet or Python function to design hundreds of elements, a single mistake in the calculation propagates to all of those element designs.

With any large or complex calculation, it is easy to make a change that affects other parts of the calculation in unexpected ways. Especially if you come back to an old calculation to adapt it for a new use case.


Why Testing Matters
-------------------

Testing your calculations can ensure accuracy and reliability in your designs especially as calculations get complex or evolve over time.

A well-tested calculation gives you confidence that

* The calculation is working as expected for all the unique cases
* When you make a change to one equation, all the rest of the calculation still behaves as expected

In the world of software development, testing is a well-established discipline, and we can apply similar principles to our engineering calculations.


How To Test Your Calculations
-----------------------------

`CalculationRunner` provides a straightforward and effective way to run calculations with any given inputs and get the results.

1. **Define Your Calculation Function**: Take any efficalc calculation function that you want to write a test for:

.. code-block:: python

    def calc_function():
        a = Input("a", 4, "in")
        Calculation("calc", a ** 2, "in^2", result_check=True)

2. **Write Your Test**: Next, create a test case that uses `CalculationRunner` to run your calculation function with specific inputs. Then, use assertions to verify the results.

.. code-block:: python

    def test_calc_function():
        inputs = {"a": 5}
        calculation = CalculationRunner(calc_function_simple, inputs)
        results = calculation.get_results_as_dict()
        assert results["calc"].result() == 25

3. **Running Your Tests**: With your tests defined, you can run them using pytest or any other Python testing framework you prefer. Regularly running your tests after any changes to your calculations ensures ongoing accuracy and reliability.

