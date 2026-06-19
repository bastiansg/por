.PHONY: core-build app-build devcontainer-build cmtv-disk-urls camera-memory-free run-text-oracle


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


camera-memory-free:
	sudo fuser -k /dev/video* /dev/media* /dev/dma_heap/* 2>/dev/null || true
	sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'


create-qdrant-collections:
	docker compose -f .devcontainer/docker-compose.yml run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m por.scripts.qdrant.create_collections" por-devcontainer

run-text-oracle:
	docker compose -f .devcontainer/docker-compose.yml run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m por.scripts.multi_agent.run_text_oracle" por-devcontainer
