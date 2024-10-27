.PHONY: tests build publish docs

build:
	python -m build

publish:
	python -m twine upload --skip-existing dist/*

# within venv
tests:
	python -m pytest tests

# within venv
docs:
	sphinx-build docs_src docs

# within venv
sections:
	python -m "build_section_tables.py"
