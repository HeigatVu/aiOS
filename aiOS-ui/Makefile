-include .env

# Detect Operating System for Cross-Platform compatibility
UNAME_S := $(shell uname -s 2>/dev/null || echo Windows)
ifeq ($(findstring MINGW,$(UNAME_S)),MINGW)
    IS_WINDOWS := 1
else ifeq ($(findstring MSYS,$(UNAME_S)),MSYS)
    IS_WINDOWS := 1
else ifeq ($(UNAME_S),Windows)
    IS_WINDOWS := 1
endif

ifdef IS_WINDOWS
    USER_ID ?= 1000
    GROUP_ID ?= 1000
else
    USER_ID ?= $(shell id -u 2>/dev/null || echo 1000)
    GROUP_ID ?= $(shell id -g 2>/dev/null || echo 1000)
endif

export USER_ID GROUP_ID

.PHONY: install setup up up-gpu down build shell logs restart help

# Default target
all: help

install: setup

setup:
ifdef IS_WINDOWS
	powershell -ExecutionPolicy Bypass -File install.ps1
else
	bash install.sh
endif

up:
	docker compose up -d --wait

up-gpu:
	docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --wait

build:
	docker compose build

down:
	docker compose down

restart:
	docker compose restart control agent-runtime hermes-webui

shell:
	docker compose exec agent-runtime zsh

logs:
	docker compose logs -f

help:
	@echo "aiOS-ui Cross-Platform Management Commands:"
	@echo "  make install    - Run auto-installer script (creates directories, .env, builds & boots)"
	@echo "  make up         - Start the local Compose service stack"
	@echo "  make up-gpu     - Start with the NVIDIA Compose override"
	@echo "  make down       - Stop all services"
	@echo "  make build      - Rebuild service images"
	@echo "  make shell      - Attach a shell in agent-runtime"
	@echo "  make logs       - Tail all service logs"
