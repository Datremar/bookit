# Bookit

A full booking solution to manage and grow your business.
Packed with all the tools you need to boost sales, manage your calendar and
retain clients so you can focus on what you do best.

## Setup Dev Environment

This project need a database and two web server, one for the python API and the
second one for the nginx web server that displays the frontend.

Firstly, you need to create a `.env` file with all the settings you prefer.
An easy way to do it is to just copy the demo file:

```bash
cp .env_demo .env
```

All these containers are provisioned using docker. To start the dev environment
just run:

```bash
docker compose up -d
```

Your developer environment should be up and runing, check:

- API: http://127.0.0.1:8181/healthcheck/
- FrontEnd: http://127.0.0.1:8080/

**Usefull commands**:

- Turn on: `docker compose up -d`
- Turn off: `docker compose down`
- Migrations: `docker exec -it bookit-api dbmate --help`
- API lint: `docker exec bookit-api pylint "*"`
- API tests: `docker exec bookit-api python -m unittest discover -s tests -p "*.py" -v`
- SQL lint: `docker exec bookit-api sqlfluff lint migrations --dialect mysql`
- Container logs: `docker compose logs -f`

## Migrations

The project database is set up using
[Dbmate migrations](https://github.com/amacneil/dbmate), to execute the
migrations run:

```bash
docker exec -it bookit-api dbmate up
```

Any changes to the database should be provisioned using migrations. To
better understand now to create a new migration, please follow the 
[Dbmate docs](https://github.com/amacneil/dbmate/blob/main/README.md)

## API [![Code Quality & Tests](https://github.com/mariogarridopt/bookit/actions/workflows/code-checks.yml/badge.svg?branch=master)](https://github.com/mariogarridopt/bookit/actions/workflows/code-checks.yml)

The python API is running on port `8181` so you can access it at:
`http://localhost:8181/`.

A health check endpoint is provided so that you can check if everything is
running smoothly: http://localhost:8181/healthcheck

### Token

All the API functions that have the decorators `@login_required` or `@admin_required` required a token when been called.

For example, everyone can call **GET** /auth/token, but only logged-in users can call **GET** /auth. For the endpoints that require login, a token should be provided as Bearer Authentication. Some cURL Examples:

**GET** /auth/token

```bash
curl --request GET \
  --url 'http://127.0.0.1:8181/auth/token?username=admin&password=admin'
```

**GET** /auth

```bash
curl --request GET \
  --url http://127.0.0.1:8181/auth \
  --header 'Authorization: Bearer 8so3DdfsciqCS0BqocChiQ'
```

## Frontend

The app frontend will run on port `8080`so you can access it at:
`http://localhost:8080/`.

![demo img](demo.jpg)

## Contribute

If you want to contribute, please check the [CONTRIBUTING.md](CONTRIBUTING.md) page.
