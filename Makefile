VENV = .venv

.PHONY: $(VENV) install build upload clean confirm

build: install
	$(VENV)/bin/python -m build

install: $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/pip install --upgrade build setuptools

upload: confirm build
	# Check credentials to PyPI in $HOME/.pypirc
	$(VENV)/bin/pip install --upgrade twine
	$(VENV)/bin/python -m twine upload dist/*

clean:
	rm -Rf dist $(VENV)

$(VENV):
	python3 -m venv $(VENV)

confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

test:
	python3 -m unittest discover -s tests