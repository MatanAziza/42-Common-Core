install:
	python3 -m venv venv_flyin;
	source venv_flyin/bin/activate;
	pip install pydantic;

lint:
	flake8 srcs;
	mypy --strict srcs;
	flake8 fly_in.py;
	mypy --strict fly_in.py;

clean:
	rm -rf venv_flyin
