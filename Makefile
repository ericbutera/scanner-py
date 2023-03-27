SHELL:=/bin/bash

include .env
export

IMAGE_NAME=scanner-py
IMAGE_REPO=ghcr.io/ericbutera
IMAGE_TAG=v0.0.1
# IMAGE_TAG=latest

.DEFAULT_GOAL := help

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: image-build
image-build: ## Build docker image
	docker build -t ${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} .

.PHONY: image-buildx-init
image-buildx-init: ## Init buildx; prereq for image-buildx
	docker buildx create --name builder
	docker buildx use builder
	docker buildx inspect --bootstrap

.PHONY: image-buildx
image-buildx: ## Build multiarch & push to container registry
	docker buildx build --platform linux/amd64,linux/arm64 -t ${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} --push .

.PHONY: image-push
 image-push: ## Push docker image
	docker push ${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

.PHONY: image-run
image-run: ## Run docker image
	docker run -it --rm ${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}


.PHONY: run
run: ## Run the serial demo
	poetry run python main.py

.PHONY: run-worker-pool
run-worker-pool: ## Run the worker pool demo
	poetry run python worker_pool.py

.PHONY: run-async
run-async: ## Run the async demo
	poetry run python async.py

.PHONY: run-async-pool
run-async-pool: ## Run the async pool demo
	poetry run python async_pool.py