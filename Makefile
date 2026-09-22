CONFIG = config.txt
MAIN = a_maze_ing.py

install:

run:
	python3 ${MAIN} ${CONFIG}

debug:
	python3 -m pdb ${MAIN} ${CONFIG}

clean:
	find . -type d -name "__pycache__" rm -rf# -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint
