all: install run

install:
	python3 -m venv venv_flyin;
	source venv_flyin/bin/activate &&\
	pip install -r requirements.txt;

run:
	source venv_flyin/bin/activate &&\
	python3 fly_in.py

debug:
	source venv_flyin/bin/activate && python3 -m pdb fly_in.py

lint:
	flake8 srcs;
	mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs srcs;
	flake8 fly_in.py;
	mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs fly_in.py;

lint-strict:
	flake8 srcs;
	mypy --strict srcs;
	flake8 fly_in.py;
	mypy --strict fly_in.py;

clean:
	rm -rf venv_flyin
