.PHONY: help env
.DEFAULT_GOAL := help

IMAGE_TAG = registry.heroku.com/mc-dokaben/web

usage:
	@echo "USAGE:"
	@echo "    make build"

build: ## build Docker image
	docker build -t $(IMAGE_TAG) .

server:
	docker run -p 5000:5000 -e PORT=5000 -d $(IMAGE_TAG):latest

server_local:
	poetry run gunicorn --bind 0.0.0.0:5001 --chdir webapp app:app &

help: ## help lists
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
