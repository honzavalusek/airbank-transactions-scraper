.PHONY: install run

install:
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install -r requirements.txt
	playwright install

run:
	python3 src/main.py