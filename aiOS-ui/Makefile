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

.PHONY: install setup up up-gpu down build shell root-shell logs restart help

# Default target
all: help

install: setup

setup:
ifdef IS_WINDOWS
	powershell -ExecutionPolicy Bypass -File install.ps1
else
	bash install.sh
endif

up: build
	docker compose up -d

up-gpu: build
	docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d

build:
	docker compose build

down:
	docker compose down

restart:
	docker compose restart sandbox

shell:
	docker compose exec --user $(USER_ID) sandbox zsh

root-shell:
	docker compose exec --user root sandbox zsh

logs:
	docker compose logs -f sandbox

help:
	@echo "aiOS-ui Cross-Platform Management Commands:"
	@echo "  make install    - Run auto-installer script (creates directories, .env, builds & boots)"
	@echo "  make up         - Build and start container (Universal CPU/Metal mode)"
	@echo "  make up-gpu     - Build and start container with NVIDIA GPU passthrough"
	@echo "  make down       - Stop container"
	@echo "  make build      - Rebuild container"
	@echo "  make shell      - Attach interactive zsh shell as user ($(USER_ID))"
	@echo "  make root-shell - Attach interactive zsh shell as root"
	@echo "  make logs       - Tail container logs"
