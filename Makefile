VENV = .venv

.PHONY: install build upload clean

build: $(VENV)
	$(VENV)/bin/python setup.py sdist

install: $(VENV)
	$(VENV)/bin/pip install --upgrade build setuptools

upload: build
	$(VENV)/bin/pip install --upgrade twine
	$(VENV)/bin/python -m twine upload dist/*

clean:
	rm -Rf dist $(VENV)

$(VENV):
	python3 -m venv $(VENV)
	$(MAKE) install
