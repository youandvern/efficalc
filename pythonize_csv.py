import csv

from efficalc.sections.aisc_wide_flange import WideFlange


def get_all_sizes_from_csv(filepath, output_filepath):
    """
    This method reads the csv section property files and generates a Python list of all the section size names from the
    AISC_name column.

    :param filepath: the path to the csv file
    :type filepath: str
    :param output_filepath: the path to the output Python file
    :type output_filepath: str
    :return: None
    """
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
        r"efficalc\sections\csv\aisc_sections_WF.csv",
        r"all_sections.py",
    )
