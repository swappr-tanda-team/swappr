.DEFAULT_GOAL := build
TAG?=latest
DOCKER_MACHINE=default
DOCKER_NODE_STD_ARGS=-it --rm -v $(shell pwd):/usr/app:rw -w /usr/app -p 5000:5000
DOCKER_NODE_IMAGE=swappr-env:latest

run:
	docker run $(DOCKER_NODE_STD_ARGS) $(DOCKER_NODE_IMAGE) python runserver.py

build:
	docker build -t swappr-env:latest .