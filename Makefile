-include .env
USER_ID ?= $(shell id -u)
GROUP_ID ?= $(shell id -g)
export USER_ID GROUP_ID

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
