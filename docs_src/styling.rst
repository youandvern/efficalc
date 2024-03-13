.. _styling:

Styling Reports
===============

Variable names and units are styled with using LaTex mathematical notation. Here are some helpful tips for common use cases.

Subscripts
----------

Single character subscripts can be created with a simple underscore, "_1". For example:

    Coded Definition: :code:`Input("min_a", 1, "m_2")`

    Display Result:   min\ :sub:`a`\ = 1 m\ :sub:`2`\

Multiple character subscripts must be wrapped in curly braces after the underscore character "_{more}". For example:

    Coded Definition: :code:`Input("min_{abc}", 1, "m_{123}")`

    Display Result:   min\ :sub:`abc`\ = 1 m\ :sub:`123`\

Superscripts
------------

Single character superscripts can be created with a simple caret (circumflex), "^1". For example:

   Coded Definition: :code:`Input("min^a", 1, "m^2")`

   Display Result:   min\ :sup:`a`\ = 1 m\ :sup:`2`\

Multiple character superscripts must be wrapped in the curly braces after the caret character "^{more}". For example:

   Coded Definition: :code:`Input("min^{abc}", 1, "m^{123}")`

   Display Result:   min\ :sup:`abc`\ = 1 m\ :sup:`123`\

Greek Letters and Symbols
-------------------------

Greek letters and symbols are added with standard LaTex notation and can be combined with any other notations (such as subscripts and superscripts).
Many of the most common letters and symbols are listed at https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols.

For example,

   Coded Definition: :code:`Input("\\phi_m", 0.9)`

   Display Result:   :math:`\phi`\ :sub:`m`\ = 0.9


Adding Spaces
-------------

LaTex mathematical formatting naturally squashes spaces in text elements. If spaces are needed within units or
variable names, then an escape sequence can be used with a forward slash before the space "\ ". For example:

   Coded Definition: :code:`Input("min\\ abc", 1, "m\\ 123")`

   Display Result:   min abc = 1 m 123
