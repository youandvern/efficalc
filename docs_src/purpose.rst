.. _purpose:

Purpose and Background
======================

* Things we don't like about excel but like about python table


Efficalc was developed to provide a robust, flexible, and efficient alternative to traditional calculation methods like Excel, which has remained the industry standard for decades. While Excel is versatile and used in many different industries, it is limited in its ability to integrate with modern engineering workflows. Furthermore, as a general tool, it's not particularly good at any one thing, especially providing a tailored experience for engineering work.

Here are a few things we don't like about excel calculations, and wanted to fix with efficalc.

Finding mistakes
----------------

There are many times we have to review calculations, such as

#. Debugging our own calculations as we write them
#. Understanding the calculations that a colleague shares with you to use
#. Modifying an old calculation that you want to repurpose for a slightly different scenario

When these calculations are hard-to-follow, it gets in the way of our work. Not only is it tedious and annoying, but it can lead to mistakes in our work that cost us time, reputation, and potentially our license.

There are also many times when others review our calculations:

#. Check-in reviews by a project lead
#. Official peer reviews
#. Submittal reviews

In these cases, hard-to-follow or error-ridden calculations have a host of other implications including costly time delays and loss of rapport with important clients.

When you consider looking for mistakes, which of these is easier to understand?

###INSERT IMAGE OF LTB EQUATION EXCEL VS EFFICALC###


Automation and Scalability
--------------------------

Imagine this common scenario, you need to design all the steel floor beams in a building, so you get your favorite beam design spreadsheet go through the process of inputting the unique dimensions/loads, copying the spreadsheet for the next beam, and so on...

But then, you realize there's a mistake in one of the cell calculations, or maybe there's a change to the type of steel that's available. To update the calculations, you have to go back through every spreadsheet and make the same exact update.

However, if your design spreadsheet is actually a python function, then you can update that one calculation function. Then you can re-run it for all of your unique inputs, and every beam is re-calculated to with your updates.

    .. code-block:: python
        :linenos:

        all_beam_configurations = [
            ["Beam #1", 12, 3.34, 50],
            ["Beam #4", 15, 2.55, 50],
            ["Beam #3", 34, 1.25, 50],
            ...
        ]


        def beam_calculation(name, span, ultimate_load, steel_strength):
            # insert your design calculations here
            # make updates in this one function to update all designs


        def design_all_beams():
            for configuration in all_beam_configurations:
                result = beam_calculation(*configuration)
                print(result)

            return "Design complete"


Formatting and Submittal
------------------------

At the end of most projects, a calculation report is submitted and reviewed by an independent authority. When you print a spreadsheet however, there's nothing to review! It's just a bunch of numbers that may be right or may not be.

Often to facilitate a proper review and documentation of the design, spreadsheet calculations have to be manually formatted by the engineer. It's tedious, time-consuming, and just not a good use of our time.

By automating the calculation report creation in a highly detailed and readable way, efficalc enables engineers to spend more time doing what they're good at: engineering. So spend less time manually formatting calcs, and focus on the actual calculations and designs!

### INSERT IMAGE OF SPREADSHEET CALC ###


Modern Workflows
----------------

These days, there's so many new workflows with increased automation whether it's using the CSI OAPI to automate ETABS analysis or Grasshopper/Rhino scripts for parametric modelling.

Excel often times has a hard time integrating into these workflows without a lot of copy/pasting of date and manual intervention.

Python-native calculations enable you to plug into your automation workflows directly and completely bypass the friction of getting data in and out of excel.

Not to mention, Python is the ideal language for working with large amounts of data. With pandas, NumPy, matplotlib, and others, managing large data sets in Python saves a lot of headache vs trying to manage it in excel.


A New Era
---------

Efficalc aims to set a new standard for how calculations are created and shared in the engineering community. By shifting from spreadsheet-based methods to a code-driven approach, efficalc empowers users to build more readable, scalable, and reliable design calculations.

This transition not only improves the quality of engineering designs but facilitates better communication, understanding, and efficiency among teams and stakeholders.

So, **give it a try!**

