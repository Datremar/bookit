.PHONY: up down logs lint test

up:
	docker compose up -d

down: 
	docker compose down

logs:
	docker compose logs -f

lint:
	pylint --rcfile api/.pylintrc "api/*"

test:
	python -m unittest discover -s api/tests -p "*.py" -v
