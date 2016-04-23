.DEFAULT_GOAL := build
TAG?=latest
DOCKER_MACHINE=default
DOCKER_NODE_STD_ARGS=-it --rm -v $(shell pwd):/usr/app:rw -w /usr/app -p 9000:9000 -e "SWAPPR_SECRET_KEY=$$SWAPPR_SECRET_KEY" -e "SWAPPR_TANDA_API_KEY=$$SWAPPR_TANDA_API_KEY" -e "SWAPPR_TANDA_GOD_TOKEN=$$SWAPPR_TANDA_GOD_TOKEN" -e "SWAPPR_TANDA_API_SECRET=$$SWAPPR_TANDA_API_SECRET" -e "REDIRECT_URI=http://docker:9000/user/authorize"
DOCKER_NODE_IMAGE=swappr-env:latest
PRODUCTION_CONTAINER_NAME=swappr_deployed

run:
	docker run $(DOCKER_NODE_STD_ARGS) $(DOCKER_NODE_IMAGE) python runserver.py

build:
	docker build -t swappr-env:latest .

setupDb:
	docker run $(DOCKER_NODE_STD_ARGS) $(DOCKER_NODE_IMAGE) python createDB.py

firstDeploy:
	eval $$(triton env --docker) && \
	docker pull davefinster/swappr:latest && \
	docker run -d -p 9000:9000 -e "SWAPPR_SECRET_KEY=$$SWAPPR_SECRET_KEY" -e "SWAPPR_TANDA_API_KEY=$$SWAPPR_TANDA_API_KEY" -e "SWAPPR_TANDA_GOD_TOKEN=$$SWAPPR_TANDA_GOD_TOKEN" -e "SWAPPR_TANDA_API_SECRET=$$SWAPPR_TANDA_API_SECRET" --name $(PRODUCTION_CONTAINER_NAME) -l "triton.cns.services=swappr" -e "REDIRECT_URI=http://swappr.docketbook.io/user/authorize" davefinster/swappr:latest

deploy:
	eval $$(triton env --docker) && \
	docker stop $(PRODUCTION_CONTAINER_NAME) && \
	docker rm $(PRODUCTION_CONTAINER_NAME) && \
	docker pull davefinster/swappr:latest && \
	docker run -d -p 9000:9000 -e "SWAPPR_SECRET_KEY=$$SWAPPR_SECRET_KEY" -e "SWAPPR_TANDA_API_KEY=$$SWAPPR_TANDA_API_KEY" -e "SWAPPR_TANDA_GOD_TOKEN=$$SWAPPR_TANDA_GOD_TOKEN" -e "SWAPPR_TANDA_API_SECRET=$$SWAPPR_TANDA_API_SECRET" --name $(PRODUCTION_CONTAINER_NAME) -l "triton.cns.services=swappr" -e "REDIRECT_URI=http://swappr.docketbook.io/user/authorize" davefinster/swappr:latest