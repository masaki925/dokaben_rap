.PHONY: help env
.DEFAULT_GOAL := help

IMAGE_NAME = gcr.io/$(GCP_PROJ_ID)/mc_dokaben
IMAGE_TAG  = latest

APP_HOST = http://localhost
APP_PORT = 5000
APP_EP   = rap
QUERY   = おまえの母ちゃんでべそ おまえの父ちゃん寝ゲロ

test: ## APP_HOST, APP_PORT, APP_EP
	curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{ \"verse\": \"$(QUERY)\" }" $(APP_HOST):$(APP_PORT)/$(APP_EP)

build_image: ## build Docker image
	docker build -t $(IMAGE_NAME) .

push_image: ## push Docker image to GCR
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

server: ## server (IMAGE_NAME)
	docker run -p 5000:5000 -e PORT=5000 -d $(IMAGE_NAME):$(IMAGE_TAG)

server_local: ## server local
	poetry run gunicorn --bind 0.0.0.0:5001 --chdir webapp --timeout 300 --reload app:app &

help: ## help lists
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
