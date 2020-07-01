doc:
	pdoc --html sudoku --html-dir public
	mv public/sudoku/index.html public/index.html
	rm -rf public/sudoku

install:
	pip install .

dist:
	python3 setup.py sdist bdist_wheel

release:
	python3 -m twine upload dist/*