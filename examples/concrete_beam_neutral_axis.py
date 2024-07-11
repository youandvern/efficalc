from efficalc import Calculation, Comparison, Heading, Input, TextBlock, Title


def calculation():

    Title("Concrete Beam Neutral Axis")
    TextBlock("Determine the neutral axis depth in a singly reinforced concrete beam.")

    Heading("Inputs")
    As = Input("A_s", 3, "in^2", description="Area of reinforcing steel")
    fy = Input("f_y", 50, "ksi", "Yield strength of reinforcing steel")
    fc = Input("f'_c", 4, "ksi", "Concrete compressive strength")
    b = Input("b", 12, "in", "Beam width")
    B1 = Input("\\beta_1", 0.85, description="Compressive stress block ratio")

    Heading("Calculations")
    a = Calculation("a", As * fy / (0.85 * fc * b), "in", result_check=True)
    c = Calculation(
        "c",
        a / B1,
        "in",
        result_check=True,
        description="Neutral axis depth",
        reference="ACI 318-14 22.2.2.4.1",
    )

    Comparison(c, ">", 3.5, result_check=True)
