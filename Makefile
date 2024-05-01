all: help

.PHONY: help
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: replace-env
replace-env:  ## Use to update existing .env with .env.example
	cp .env.example .env

.env:  ## Copy .env.example to .env
	cp .env.example .env


install: .env  ## Install dependencies
	poetry install

setup:

clean:

build: .env
	docker-compose -f deploy/docker/docker-compose.yml --project-directory . build

kill:  ## Kill all running containers
	docker kill $$(docker ps -a -q)



run: build   ## Run the project
	@echo "Stopping and removing current containers and volumes..."
	docker-compose -f deploy/docker/docker-compose.yml --project-directory . down -v
	@echo "Building and starting new containers..."
	docker-compose -f deploy/docker/docker-compose.yml --project-directory . up -d
	docker-compose -f deploy/docker/docker-compose.yml -f deploy/docker/docker-compose.local.yml --project-directory . up

reboot: kill run  ## Kill all running containers and run the project

.PHONY: show-envs-info
show-envs-info:  ## Show information about environment variables used by the application. Also you can specify format using FORMAT variable. Like: make show-envs-info FORMAT="markdown"
	@python scripts/print_env_vars.py $(FORMAT)

.PHONY: remove
remove:
	docker-compose -f deploy/docker/docker-compose.yml --project-directory . rm
