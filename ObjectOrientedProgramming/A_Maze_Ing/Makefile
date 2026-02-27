all:
	echo 'No command for "all". Please run with command "make run"'

install:
	echo 'No dependencies needed. Please run with command "make run"'

run:
	python3 a_maze_ing.py config.txt

debug:
	python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ maze.txt

lint:
	flake8 . & mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . & mypy . --strict

.PHONY: all install run debug clean lint lint-strict
