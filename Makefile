.PHONY: setup test demo

setup:
	python3 -m venv .venv
	. .venv/bin/activate; pip install -U pip
	. .venv/bin/activate; pip install -e .[dev]

test:
	. .venv/bin/activate; pytest -q

demo:
	. .venv/bin/activate; python -m igsimplex --config configs/var_only.yaml --seed 42

