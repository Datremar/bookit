.PHONY: up down logs lint test mysql-lint

up:
	docker compose up -d

down: 
	docker compose down

logs:
	docker compose logs -f

lint:
	pylint --rcfile api/.pylintrc "api/*"

mysql-lint:
	sqlfluff lint api/migrations --dialect mysql

test:
	python -m unittest discover -s api/tests -p "*.py" -v
