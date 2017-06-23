OWNER=karimtabet
IMAGE_NAME=papusa
QNAME=$(OWNER)/$(IMAGE_NAME)

BUILD_TAG=$(QNAME):0.1.$(TRAVIS_BUILD_NUMBER)
LATEST_TAG=$(QNAME):latest

.PHONY: build start

build:
	echo "Building images with Docker Compose"
	docker-compose build

start:
	echo "Starting containers with Docker Compose"
	docker-compose up -d

tag:
	echo "Tagging image with version and Travis build"
	docker tag $(LATEST_TAG) $(BUILD_TAG)

clean:
	echo "Cleaning up papusa services"
	docker rm -f papusa_nginx papusa_web papusa_redis papusa_db
	docker rmi karimtabet/papusa

test: build start
	echo "Running test script"
	sleep 20
	./acceptance_test.sh

login:
	@docker login -u "$(DOCKER_USER)" -p "$(DOCKER_PASS)"

push: login
	docker push $(BUILD_TAG)
	docker push $(LATEST_TAG)
