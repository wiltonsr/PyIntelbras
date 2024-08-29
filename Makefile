VENV = .venv

.PHONY: install build upload clean confirm

build: $(VENV)
	$(VENV)/bin/python setup.py sdist

install: $(VENV)
	$(VENV)/bin/pip install --upgrade build setuptools

upload: confirm build
	# Check credentials to PyPI in $HOME/.pypirc
	$(VENV)/bin/pip install --upgrade twine
	$(VENV)/bin/python -m twine upload dist/*

clean:
	rm -Rf dist $(VENV)

$(VENV):
	python3 -m venv $(VENV)
	$(MAKE) install

confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]