.PHONY: tests build publish docs

build:
	python -m build

tests:
	pytest

publish:
	python -m twine upload --skip-existing dist/*

docs:
	sphinx-build docs_src docs
