UID := $(shell id -u)
GID := $(shell id -g)
export UID GID

.PHONY: up down build shell logs restart

up: build
	docker compose up -d

build:
	docker compose build

down:
	docker compose down

restart:
	docker compose restart sandbox

shell:
	docker compose exec sandbox zsh

logs:
	docker compose logs -f sandbox
