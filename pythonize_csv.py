import csv

from efficalc.sections.aisc_wide_flange import WideFlange


def csv_to_python_dictionary(filepath, output_filepath):
    contents = ""
    contents += "{"
    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            contents += f'"{row["AISC_name"]}": WideFlange('
            for key, val in row.items():
                try:
                    contents += (
                        f"{key}={float(val) if key in WideFlange.number_fields else f'"{val}"'}, "
                    )
                except ValueError as e:
                    print(f"Cannot convert value: {val} to number for field {key} on row {row["AISC_name"]}")
                    raise e
            contents += f"),\n"

    contents += "}"

    # Write the string to a Python file as a static variable
    with open(output_filepath, "w", encoding="utf-8") as py_file:
        py_file.write(contents)

def get_all_sizes_from_csv(filepath, output_filepath):
    contents = ""
    contents += "("
    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            contents += f'"{row["AISC_name"]}",\n'

    contents += ")"

    # Write the string to a Python file as a static variable
    with open(output_filepath, "w", encoding="utf-8") as py_file:
        py_file.write(contents)


if __name__ == "__main__":
    get_all_sizes_from_csv(
        r"C:\Users\youan\Documents\efficalc\efficalc\sections\csv\aisc_sections_WF.csv",
        r"C:\Users\youan\Documents\efficalc\all_sections.py",
    )
