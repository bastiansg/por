.PHONY: core-build app-build devcontainer-build


core-build:
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

redis-restart: redis-stop
	docker compose up -d por-redis


qdrant-start:
	docker compose up -d por-qdrant

qdrant-stop:
	docker compose stop por-qdrant

qdrant-flush: qdrant-stop
	sudo rm -r ./resources/db/qdrant
	$(info *** WARNING you are deleting all data from qdrant ***)
	docker compose up -d por-qdrant

qdrant-restart: qdrant-stop qdrant-start


app-build: core-build
	docker compose build por-app

app-run: app-build
	docker compose  run --rm por-app

app-up: app-build
	docker compose up -d por-app

app-stop:
	docker stop por-app

app-restart: app-stop app-up


mcp-build:
	docker compose build por-mcp

mcp-start: mcp-build
	docker compose up -d por-mcp

mcp-stop:
	docker stop por-mcp

mcp-restart: mcp-stop mcp-start
