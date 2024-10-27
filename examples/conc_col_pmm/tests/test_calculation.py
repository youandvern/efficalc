import matplotlib
import pytest

from efficalc import Calculation, clear_saved_objects
from efficalc.calculation_runner import CalculationRunner

from ..calc_document.calculation import calculation
from ..calc_document.column_inputs import ColumnInputs

matplotlib.use("Agg")  # Use a non-interactive backend


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


def get_calc_by_name(all_items, name):
    for item in all_items:
        if isinstance(item, Calculation) and item.name == name:
            return item


def assert_calc_value(calc: Calculation, expected: float):
    assert calc.result() == pytest.approx(expected, abs=0.001)


def test_calc_with_defaults(common_setup_teardown):
    runner = CalculationRunner(calculation)
    all_obj = runner.calculate_all_items()

    ppn = get_calc_by_name(all_obj, "{\\phi}P_n")
    pmx = get_calc_by_name(all_obj, "{\\phi}M_{nx}")
    pmy = get_calc_by_name(all_obj, "{\\phi}M_{ny}")
    dcr_mx = get_calc_by_name(all_obj, "DCR_{Mx}")
    dcr_my = get_calc_by_name(all_obj, "DCR_{My}")
    dcr_p = get_calc_by_name(all_obj, "DCR_{P}")

    assert_calc_value(ppn, 3579.613)
    assert_calc_value(pmx, 238.932)
    assert_calc_value(pmy, 119.412)
    assert_calc_value(dcr_mx, 0.837060)
    assert_calc_value(dcr_my, 0.837060)
    assert_calc_value(dcr_p, 0.838079)


def test_calc_with_custom_load_case(common_setup_teardown):
    loads = [[500, 400, 50, "yes"]]
    runner = CalculationRunner(lambda: calculation(default_loads=loads))
    all_obj = runner.calculate_all_items()

    ppn = get_calc_by_name(all_obj, "{\\phi}P_n")
    pmx = get_calc_by_name(all_obj, "{\\phi}M_{nx}")
    pmy = get_calc_by_name(all_obj, "{\\phi}M_{ny}")
    dcr_mx = get_calc_by_name(all_obj, "DCR_{Mx}")
    dcr_my = get_calc_by_name(all_obj, "DCR_{My}")
    dcr_p = get_calc_by_name(all_obj, "DCR_{P}")

    assert_calc_value(ppn, 2140.047)
    assert_calc_value(pmx, 1712.806)
    assert_calc_value(pmy, 214.404)
    assert_calc_value(dcr_mx, 0.23353)
    assert_calc_value(dcr_my, 0.23320)
    assert_calc_value(dcr_p, 0.23364)


def test_calc_with_small_column(common_setup_teardown):
    loads = [[18.22, 1.56, 3.03, "yes"]]
    col = ColumnInputs(4, 6, "#4", 1, 2, 3, 4000, 40, True, True)
    runner = CalculationRunner(lambda: calculation(default_loads=loads, col=col))
    all_obj = runner.calculate_all_items()

    ppn = get_calc_by_name(all_obj, "{\\phi}P_n")
    pmx = get_calc_by_name(all_obj, "{\\phi}M_{nx}")
    pmy = get_calc_by_name(all_obj, "{\\phi}M_{ny}")
    dcr_mx = get_calc_by_name(all_obj, "DCR_{Mx}")
    dcr_my = get_calc_by_name(all_obj, "DCR_{My}")
    dcr_p = get_calc_by_name(all_obj, "DCR_{P}")

    assert_calc_value(ppn, 26.6350)
    assert_calc_value(pmx, 2.28086)
    assert_calc_value(pmy, 4.43000)
    assert_calc_value(dcr_mx, 0.68395)
    assert_calc_value(dcr_my, 0.68397)
    assert_calc_value(dcr_p, 0.68406)
