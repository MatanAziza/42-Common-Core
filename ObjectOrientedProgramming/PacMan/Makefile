all: install run

install:
	python3 -m venv env;source env/bin/activate &&\
	python -m pip install -r requirements.txt

run:
	source env/bin/activate; python3 pacman.py config.json

build:
	python3 -m venv build_env &&\
	source build_env/bin/activate &&\
	python -m pip install -r requirements.txt &&\
	python -m pip install pyinstaller &&\
	pyinstaller pacman.py

debug:
	source env/bin/activate; python3 -m pdb pacman.py config.json

clean:
	rm -rf __pycache__ .mypy_cache env build_env

fclean: clean
	rm -rf build/ dist/ pacman.spec

lint:
	source env/bin/activate; flake8 *.py & python -m mypy *.py

lint-strict:
	source env/bin/activate; flake8 *.py & python -m mypy *.py --strict

help:
	@echo "If not present in the directory, place the mazegenerator package"
	@echo "(name looks like 'mazegenerator-xxxx.whl')"
	@echo "then run commands 'make install' followed by 'make run'."

.PHONY: all install run build debug clean fclean lint lint-strict help
