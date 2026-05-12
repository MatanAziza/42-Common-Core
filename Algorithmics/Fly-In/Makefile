all: install run

install:
	python3 -m venv venv_flyin;
	source venv_flyin/bin/activate;
	pip install -r requirements.txt;

run:
	source venv_flyin/bin/activate;
	python3 fly_in.py $(ARGS)

lint:
	flake8 srcs;
	mypy --strict srcs;
	flake8 fly_in.py;
	mypy --strict fly_in.py;

clean:
	rm -rf venv_flyin

test:
	echo @$(PARAM)
