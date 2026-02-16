NAME = a_maze_ing.py
PYTHON = python3
FLAKE8 = python3 -m flake8 .
MYPY = python3 -m mypy

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install flake8 mypy


run:
	$(PYTHON) $(NAME) config.txt


clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf maze.txt

rules:
	$(FLAKE8) .
	$(MYPY) --strict .

