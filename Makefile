.PHONY: tests build publish docs

build:
	python -m build

tests:
	python -m pytest

publish:
	python -m twine upload --skip-existing dist/*

docs:
	sphinx-build docs_src docs

sections:
	python -m "build_section_tables.py"
