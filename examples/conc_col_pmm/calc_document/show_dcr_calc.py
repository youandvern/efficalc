from efficalc import (
    Calculation,
    Comparison,
    Heading,
    TextBlock,
    absolute,
)


def show(vertical_pt, load, capacity, dcr):
    Heading("DCR Calculation", 2)
    if vertical_pt:
        TextBlock(
            "Since the load point is almost on the P axis, the DCR can be calculated by comparing the applied axial"
            " load to the axial capacity calculated above:"
        )
        if load[2] < 0:
            efficalc_cap = Calculation("{\\phi}P_{\mathrm{n,min}}", capacity, "kips")
            dcr = Calculation("DCR", load[2] / efficalc_cap)
            Comparison(dcr, "<", 1.0)
        else:
            efficalc_cap = Calculation("{\\phi}P_{\mathrm{n,max}}", capacity, "kips")
            dcr = Calculation("DCR", load[2] / efficalc_cap)
            Comparison(dcr, "<", 1.0)
    else:
        TextBlock(
            "Compare the ratios of demand to capacity for Mx, My, and P to show that the calculated capacity"
            " point is on the same PMM vector as the demand point. Note that the absolute value for the"
            " moment DCRs is because the column has equal moment capacity in opposite directions by symmetry."
        )
        Calculation("DCR_{Mx}", absolute(load[0] / capacity[0]))
        Calculation("DCR_{My}", absolute(load[1] / capacity[1]))
        Calculation("DCR_{P}", load[2] / capacity[2])
        dcr = Calculation("DCR", dcr, "", "The final DCR is:")
        Comparison(dcr, "<", 1.0, true_message="O.K.", false_message="N.G.")
