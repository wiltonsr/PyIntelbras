VENV = .venv

.PHONY: install build clean

build: $(VENV)
	$(VENV)/bin/python -m build

install: $(VENV)
	$(VENV)/bin/pip install --upgrade build

clean:
	rm -Rf dist $(VENV)

$(VENV):
	python3 -m venv $(VENV)
	$(MAKE) install
