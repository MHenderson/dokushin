doc:
	pdoc --html sussudoku --html-dir public
	mv public/sussudoku/index.html public/index.html
	rm -rf public/sussudoku

install:
	pip install .

dist:
	python3 setup.py sdist bdist_wheel

release:
	python3 -m twine upload dist/*