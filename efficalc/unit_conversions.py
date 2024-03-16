import math

from latexexpr_efficalc import PI, Variable

k_to_lb = Variable(r"1000 \ \mathrm{lbs/kip}", 1000, "lbs/kip")
"""Variable instance to show conversions from kips to lbs. (Divide by this variable to reverse the conversion)

.. code-block:: python

        >>> v = Input("v", 2, "kip")
        >>> Calculation('result',v * k_to_lb, "lbs")
        Calculation report will show --> result = v * 1000 lbs/kip = 2 kip * 1000 lbs/kip = 2000 lbs
"""

ft_to_in = Variable(r"12 \ \mathrm{in/ft}", 12, "in/ft")
"""Variable instance to show conversions from ft to in. (Divide by this variable to reverse the conversion)

.. code-block:: python

        >>> v = Input("v", 2, "ft")
        >>> Calculation('result',v * ft_to_in, "in")
        Calculation report will show --> result = v * 12 in/ft = 2 ft * 12 in/ft = 24 in
"""

deg_to_rad = Variable(r"\pi / 180 \ \mathrm{rad/deg}", math.pi / 180, "rad/deg")
"""Variable instance to show conversions from degrees to radians. (Divide by this variable to reverse the conversion)

.. code-block:: python

        >>> v = Input("v", 180, "deg")
        >>> Calculation('result',v * deg_to_rad, "rad")
        Calculation report will show --> result = v * pi / 180 rad/deg = 180deg * 3.142/180 rad/deg = 3.142 rad
"""
