.PHONY: up down logs lint test sql-lint

up:
	docker compose up -d

down: 
	docker compose down

logs:
	docker compose logs -f

lint:
	pylint --rcfile api/.pylintrc "api/*"

sql-lint:
	sqlfluff lint api/migrations

test:
	python3 -m unittest discover -s api/tests -p "*.py" -v
