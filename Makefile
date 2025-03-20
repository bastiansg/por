include .env
.PHONY: core-build devcontainer-build


core-build:
	[ -e .secrets/.env ] || touch .secrets/.env
	docker compose build istm-core

core-run:
	docker compose run istm-core


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build istm-devcontainer


redis-start:
	docker compose up -d istm-redis

redis-stop:
	docker compose stop istm-redis

redis-flush:
	docker compose exec istm-redis redis-cli FLUSHALL
