clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

install:
	poetry install

format: install
	poetry run isort app tests
	poetry run black app tests

lint: install
	poetry run isort --check app tests
	poetry run black --check app tests

test: 
	docker-compose up --build --abort-on-container-exit --force-recreate --exit-code-from tests tests; docker-compose down

run: 
	docker-compose up --build word-counter postgres

down:
	docker-compose down

SHELL := /bin/bash