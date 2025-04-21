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


qdrant-start:
	docker compose up -d por-qdrant

qdrant-stop:
	docker compose stop por-qdrant

qdrant-flush:
	sudo rm -r ./resources/db/qdrant
	$(info *** WARNING you are deleting all data from qdrant ***)

qdrant-restart: qdrant-stop qdrant-start


app-run: devcontainer-build
	docker compose -f .devcontainer/docker-compose.yml run --rm --entrypoint="python -m por.app.app" por-devcontainer
