from examples.conc_col_pmm.calc_document.document_wrapper import run


def test_document_wrapper(col_data, loads):
    run(True, col_data, loads)
