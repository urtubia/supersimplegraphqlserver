APPNAME=webapp

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
	# shell into image mounting the current directory as a volume
	docker run -it --rm -v $(PWD):/app -w /app supersimplegraphqlserver_$(APPNAME) /bin/bash

attach:
	docker exec -it supersimplegraphqlserver_$(APPNAME)_1 /bin/bash