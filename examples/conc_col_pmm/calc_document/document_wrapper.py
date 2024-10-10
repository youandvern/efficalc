from efficalc.report_builder import ReportBuilder

from .calculation import calculation as col_input_calc

# parameters: "override_inputs" is boolean and indicates whether the values
# provided in the next two arguments (column parameters, then load data)
# should override the default/user-input Input values


def run(override_inputs: bool, col_data: list, loads: list[list]):
    if override_inputs:
        new_inputs = {}

        input_to_name = {
            "w": "w",
            "h": "h",
            "bar_size": "",
            "bar_cover": " ",
            "bars_x": "    ",
            "bars_y": "     ",
            "fc": r"f^{\prime}_c",
            "fy": "f_y",
            "cover_type": "  ",
            "transverse_type": "   ",
        }
        for i in range(len(input_to_name)):
            new_inputs[input_to_name["w"]] = col_data[0]
            new_inputs[input_to_name["h"]] = col_data[1]
            new_inputs[input_to_name["bar_size"]] = col_data[2]
            new_inputs[input_to_name["bar_cover"]] = col_data[3]
            new_inputs[input_to_name["bars_x"]] = col_data[4]
            new_inputs[input_to_name["bars_y"]] = col_data[5]
            new_inputs[input_to_name["fc"]] = col_data[6]
            new_inputs[input_to_name["fy"]] = col_data[7]
            new_inputs[input_to_name["cover_type"]] = col_data[8]
            new_inputs[input_to_name["transverse_type"]] = col_data[9]

        builder = ReportBuilder(lambda: col_input_calc(default_loads=loads), new_inputs)
        builder.view_report()
    else:
        builder = ReportBuilder(col_input_calc)
        builder.view_report()
