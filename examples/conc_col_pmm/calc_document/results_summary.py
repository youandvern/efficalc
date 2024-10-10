from efficalc import Comparison, Heading, Table

from ..pmm_search.load_combo import LoadCombination

"""
Creates a table with the DCRs for all load cases. Also calculates the max
DCR, checks whether it is less than 1, and adds this to the result check. 
"""


def results_summarizer(load_combos: list[LoadCombination], dcr_results):
    Heading("Summary of Results")
    data = [
        [
            ld.p,
            ld.mx,
            ld.my,
            round(dcr_results[i], 2),
            "O.K." if dcr_results[i] < 1 else "N.G.",
        ]
        for i, ld in enumerate(load_combos)
    ]

    headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "PM Vector DCR", "Passing?"]
    Table(data, headers, "DCRs For All Load Cases", False, False)

    # calculate the max DCR and show
    max_dcr = round(max(dcr_results), 2)
    Comparison(
        max_dcr,
        "<",
        1.0,
        true_message="O.K.",
        false_message="N.G.",
        description="Max DCR check:",
        result_check=True,
    )
