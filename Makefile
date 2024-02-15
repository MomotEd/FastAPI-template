# Common

all: run

## Runs application. Builds, creates, starts, and attaches to containers for a service. | Common
run:
	docker-compose up

## Rebuild xcm_app container
build:
	docker-compose build

## Runs application on service ports.
debug:
	docker-compose run --service-ports app

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Removes stopped service containers.
clean:
	@docker-compose down

## Runs command `bash` commands in docker container.
bash:
	@docker-compose exec app sh

## Upgrade your python's dependencies:
upgrade:
	docker-compose run --rm app python3 -m $(PROJECT_NAME).helpers.development.check-requirements

test:
	@docker exec -it app pytest --cov;

# Linters & tests

## Formats code with `black`. | Linters
black:
	@docker-compose run --rm app black app --exclude app/alembic/migrations -l 79

## Formats code with `flake8`.
lint:
	@docker-compose run --rm app flake8 app

# Database

## Runs PostgreSQL UI. | Database
psql:
	@docker exec -it db psql -U postgres

## Makes migration.
migrations:
	@docker exec -it app alembic revision --autogenerate;

## Upgrades database.
migrate:
	@docker exec -it app alembic upgrade head;

## Downgrades database.
downgrade:
	@docker-compose exec app alembic downgrade -1;