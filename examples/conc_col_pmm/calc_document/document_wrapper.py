from efficalc.report_builder import ReportBuilder
from efficalc import InputTable

from .col_inputs import calculation as col_input_calc


# parameters: "override_inputs" is boolean and indicates whether the default/user-input Input values
# should be overriden by the values provided in the next two arguments (column parameters, then load data)
def run(override_inputs, col_data, loads):
    if override_inputs:
        headers = ["Pu (kip)", "Mux (kip-ft)", "Muy (kip-ft)", "Show Calc in Report"]

        # note: overriding the load table actually is not possible
        load_table = InputTable(loads, headers, "Load Cases", False, False)
        new_inputs = {"load_table": load_table}

        input_names = (
            "w",
            "h",
            "bar_size",
            "bar_cover",
            "bars_x",
            "bars_y",
            "fc",
            "fy",
            "cover_type",
            "transverse_type",
        )
        for i in range(len(input_names)):
            new_inputs[input_names[i]] = col_data[i]

        builder = ReportBuilder(col_input_calc, new_inputs)
        builder.view_report()
    else:
        builder = ReportBuilder(col_input_calc)
        builder.view_report()
