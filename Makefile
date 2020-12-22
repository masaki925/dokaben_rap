.PHONY: help env
.DEFAULT_GOAL := help

IMAGE_TAG = registry.heroku.com/mc-dokaben/web

APP_HOST = http://localhost
APP_PORT = 5000
APP_EP   = rap
QUERY   = おまえの母ちゃんでべそ おまえの父ちゃん寝ゲロ

usage:
	@echo "USAGE:"
	@echo "    make build"

test:
	curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{ \"verse\": \"$(QUERY)\" }" $(APP_HOST):$(APP_PORT)/$(APP_EP)

build: ## build Docker image
	docker build -t $(IMAGE_TAG) .

server:
	docker run -p 5000:5000 -e PORT=5000 -d $(IMAGE_TAG):latest

server_local:
	poetry run gunicorn --bind 0.0.0.0:5001 --chdir webapp --timeout 60 app:app &

help: ## help lists
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
