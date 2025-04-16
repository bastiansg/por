include .env
.PHONY: core-build devcontainer-build


core-build:
	[ -e .secrets/.env ] || touch .secrets/.env
	docker compose build por-core

core-run:
	docker compose run por-core


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build por-devcontainer


redis-start:
	docker compose up -d por-redis

redis-stop:
	docker compose stop por-redis

redis-flush:
	docker compose exec por-redis redis-cli FLUSHALL
