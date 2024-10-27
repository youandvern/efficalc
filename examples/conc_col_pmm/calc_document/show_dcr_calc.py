from latexexpr_efficalc import Variable

from efficalc import Calculation, Comparison, Heading, TextBlock, absolute, maximum

from ..pmm_search.load_combo import LoadCombination
from .column_capacities import ColumnCapacities


def show(load: LoadCombination, capacity: ColumnCapacities):

    Heading(f"DCR Calculation - Load Case #{load.id}", 2)

    only_axial = capacity.Mx.result() == 0 and capacity.My.result() == 0
    if only_axial:
        TextBlock(
            "Since the load point is on the P axis, the DCR can be calculated by comparing the applied axial"
            " load to the axial capacity calculated above:"
        )
        p = Variable("P_u", load.p, "kip")
        dcr = Calculation(
            f"DCR_{{{load.id}}}",
            absolute(p / capacity.P) if capacity.P.result() != 0 else 0,
        )
        Comparison(
            dcr,
            "<",
            1.0,
            true_message="O.K.",
            false_message="N.G.",
            description=f"Design check for load case #{load.id}",
        )

    else:
        TextBlock(
            "Compare the ratios of demand to capacity for Mx, My, and P to show that the calculated capacity"
            " point is on the same PMM vector as the demand point. Note that the absolute value for the"
            " moment DCRs is because the column has equal moment capacity in opposite directions by symmetry."
        )

        mux = Variable("M_{ux}", load.mx, "kip-ft")
        dcr_mx = Calculation(
            "DCR_{Mx}", absolute(mux / capacity.Mx) if capacity.Mx.result() != 0 else 0
        )

        my = Variable("M_{uy}", load.my, "kip-ft")
        dcr_my = Calculation(
            "DCR_{My}", absolute(my / capacity.My) if capacity.My.result() != 0 else 0
        )

        p = Variable("P_u", load.p, "kip")
        dcr_p = Calculation(
            "DCR_{P}", absolute(p / capacity.P) if capacity.P.result() != 0 else 0
        )

        dcr = Calculation(
            f"DCR_{{{load.id}}}",
            maximum(dcr_mx, dcr_my, dcr_p),
            "",
            "The final DCR is:",
        )
        Comparison(
            dcr,
            "<",
            1.0,
            true_message="O.K.",
            false_message="N.G.",
            description=f"Design check for load case #{load.id}",
        )
