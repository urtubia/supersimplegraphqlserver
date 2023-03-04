APPNAME=webapp
CURRENT_FOLDER_NAME=$(shell basename $(PWD))

# local targets
setup-local-dev:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

start:
	uvicorn src.main:app --reload

start-local: start

# docker targets
build:
	docker-compose -f docker-compose-localdev.yml build

up:
	docker-compose -f docker-compose-localdev.yml up

start-docker: build up

shell:
	docker run -it --rm -v $(PWD):/app -w /app $(CURRENT_FOLDER_NAME)_$(APPNAME) /bin/bash

attach:
	docker exec -it $(CURRENT_FOLDER_NAME)_$(APPNAME)_1 /bin/bash
